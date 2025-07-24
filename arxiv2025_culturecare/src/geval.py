import json
import os
from tqdm import trange
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from openai import OpenAI

from src.geval_prompts import *
import numpy as np

def load_dataset(cfg):
    cfg.data_path = cfg.data_path.format(data_model=cfg.data_model, strategy=cfg.strategy, culture=cfg.culture)
    print(f"Loading data file: {cfg.data_path}")
    dataset = []
    with open(cfg.data_path, 'r') as f:
        for l in f.readlines():
            dataset.append(json.loads(l))
    print(f"Size of the data {len(dataset)}")
    return dataset

class GEvaluator:
    def __init__(self, cfg):
        self.cfg = cfg

    def load_model(self):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        _model = AutoModelForCausalLM.from_pretrained(
            self.cfg.model_path,
            cache_dir="",
            local_files_only=True,
            torch_dtype=torch.float16,
            device_map="auto",
            quantization_config=quantization_config
        )
        self.model = torch.compile(_model, mode='max-autotune')
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.cfg.model_path,
            padding_side="left",
        )

    def load_gpt_model(self):
        self.model = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_evaluation_prompt(self, metric: str, post: str, response: str):
        metric_def = definition(metric)
        eval_steps = steps(metric)
        return EVAL_PROMPT.format(metric=metric, metric_def=metric_def,
                                  eval_steps=eval_steps,
                                  post=post, response=response)

    def generate_responses(self, prompts, max_new_tokens=40):
        if "gpt" in self.cfg.model_name:
            scores = []
            for prompt in prompts:
                try:
                    response = self.model.chat.completions.create(
                        model="o3-mini-2025-01-31",
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=400,
                        store=False
                        )
                    score = int(response.choices[0].message.content)
                except:
                    score = 0
                scores.append(score)
            return scores

        inputs = self.tokenizer(prompts, return_tensors="pt", padding=True, truncation=True).to("cuda")

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                return_dict_in_generate=True,
                output_scores=True,
                do_sample=False,
                temperature=1.0,
                top_p=1.0,
                top_k=0
            )
        torch.cuda.empty_cache()
        return outputs

    def get_all_emotion_metric_prompts(self, post, response):
        return [self.get_evaluation_prompt(m, post, response) for m in EMO_METRICS]

    def get_all_cultural_metric_prompts(self, post, response):
        return [self.get_evaluation_prompt(m, post, response) for m in CULT_METRICS]

    def get_all_quality_metric_prompts(self, post, response):
        return [self.get_evaluation_prompt(m, post, response) for m in OVERALL_METRICS]

    def parse_results(self, results, scores_only=False):
        scores = []
        output_strings = self.tokenizer.batch_decode(results.sequences)

        for i in output_strings:
            score_str = i.split("Evaluation score:")[-1].strip()
            if len(score_str) > 1:
                score_str = score_str[0]
            try:
                scores.append(int(score_str))
            except:
                print(f"Error when parse scores: {score_str}")
                scores.append(0)

        probs = [0] * len(scores)
        if not scores_only:
            token_idx = torch.stack([i[-1] for i in results.sequences])
            batch_indices = torch.arange(token_idx.size(0), device=token_idx.device)
            probs = results.scores[0].softmax(dim=-1)
            probs = probs[batch_indices, token_idx].cpu().detach().tolist()

        return scores, probs

    def evaluate_responses(self, dataset, scores_only=False):
        output_dir = os.path.join(self.cfg.output_dir, self.cfg.model_name, self.cfg.data_model, self.cfg.strategy)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directory '{output_dir}' created.")
        else:
            print(f"Directory '{output_dir}' already exists.")

        output_file = open(os.path.join(self.cfg.output_dir, self.cfg.model_name, self.cfg.data_model, self.cfg.strategy, f"{self.cfg.culture}_evaluation.json"), 'a')
        for idx in trange(len(dataset)):
            row = dataset[idx]
            emo_prompts = self.get_all_emotion_metric_prompts(row["post"], row["response"])
            cult_prompts = self.get_all_cultural_metric_prompts(row["post"], row["response"])
            quality_prompts = self.get_all_quality_metric_prompts(row["post"], row["response"])

            emo_results = self.generate_responses(emo_prompts)
            cult_results = self.generate_responses(cult_prompts)
            quality_results = self.generate_responses(quality_prompts)

            if "gpt" in self.cfg.model_name:
                emo_scores = emo_results
                cult_scores = cult_results
                quality_scores = quality_results
                emo_probs = [1]*len(emo_scores)
                cult_probs = [1]*len(cult_scores)
                quality_probs = [1]*len(quality_scores)
                norm_score = [score * prob for score, prob in zip(emo_scores+cult_scores+quality_scores, emo_probs+cult_probs+quality_probs)]
            else:
                emo_scores, emo_probs = self.parse_results(emo_results, scores_only)
                cult_scores, cult_probs = self.parse_results(cult_results, scores_only)
                quality_scores, quality_probs = self.parse_results(quality_results, scores_only)
                norm_score = [score * prob for score, prob in zip(emo_scores+cult_scores+quality_scores, emo_probs+cult_probs+quality_probs)]

            data_to_save = {
                "post_id": row["post_id"],
                "post": row["post"],
                "response": row["response"],
                "emo_scores": emo_scores,
                "emo_probs": emo_probs,
                "cult_scores": cult_scores,
                "cult_probs": cult_probs,
                "quality_scores": quality_scores,
                "quality_probs": quality_probs,
                "normalized_score": np.mean(norm_score),
            }
            output_file.write(json.dumps(data_to_save)+"\n")
