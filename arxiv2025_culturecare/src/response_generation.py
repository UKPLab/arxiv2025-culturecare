import json
import os
import pandas as pd
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from src.prompting_strategies import NAME2STRATEGY, NAME2CULTURE, USER_PROMPT, annotations_prompt

def load_dataset(cfg):
    cfg.data_path = cfg.data_path.format(culture=cfg.culture)
    dataset = pd.read_json(cfg.data_path, lines=True)
    print(f"Columns of the data {dataset.columns}")
    print(f"Size of the data {len(dataset)}")
    return dataset.to_dict(orient="records")

class ResponseGenerator:
    def __init__(self, cfg):
        self.cfg = cfg

    def load_model(self):
        #quantization_config = BitsAndBytesConfig(
        #    load_in_4bit=True,
        #    bnb_4bit_quant_type="nf4",
        #    bnb_4bit_use_double_quant=True,
        #    bnb_4bit_compute_dtype=torch.bfloat16,
        #)

        self.model = AutoModelForCausalLM.from_pretrained(
            self.cfg.model_path,
            cache_dir="",
            local_files_only=True,
            torch_dtype=torch.float16,
            device_map="auto",
        #    quantization_config=quantization_config
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.cfg.model_path,
            padding_side="left",
        )

    def _generate(self, prompt):
        self.model.eval()
        prompt = self.tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True)
        if self.tokenizer.bos_token:
            prompt = prompt.replace(self.tokenizer.bos_token, "")
            prompt_tokenized = self.tokenizer.encode(prompt, return_tensors="pt").to(self.model.device)

        prompt_tokenized = self.tokenizer.encode(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            output_tokenized = self.model.generate(prompt_tokenized, pad_token_id=self.tokenizer.eos_token_id,
                                                   **self.cfg.generate_cfg)

        output = self.tokenizer.decode(output_tokenized[0], skip_special_tokens=True)
        output_o = output.replace(str(self.tokenizer.bos_token), "").replace(str(self.tokenizer.eos_token), "").strip()
        model_prompt_o = prompt.replace(str(self.tokenizer.bos_token), "").replace(str(self.tokenizer.eos_token),
                                                                                   "").strip()
        response = output_o.replace(model_prompt_o, "", 1)
        return response.split("**Response**:")[-1].lstrip('assistant_').lstrip("assistant").strip()

    def _get_user_prompts(self, datapoint):
        if "annotation" in self.cfg.strategy:
            user_prompt = annotations_prompt(datapoint)
        else:
            user_prompt = USER_PROMPT.format(post=datapoint["post"]["text"])
        return user_prompt

    def _get_prompts(self, datapoint):
        culture = NAME2CULTURE.get(self.cfg.culture.lower(), self.cfg.culture)
        strategy_template = NAME2STRATEGY.get(self.cfg.strategy)
        sys_prompt = strategy_template.format(culture=culture)
        user_prompt = self._get_user_prompts(datapoint)

        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def generate_response(self, dataset):
        output_dir = os.path.join(self.cfg.output_dir, self.cfg.model_name, self.cfg.strategy)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directory '{output_dir}' created.")
        else:
            print(f"Directory '{output_dir}' already exists.")

        output_file = open(os.path.join(self.cfg.output_dir, self.cfg.model_name, self.cfg.strategy, f"{self.cfg.culture}_response.json"), 'a')

        for idx, datapoint in enumerate(dataset):
            if idx % 5 == 0:
                print(f"Current progress: {idx}")
            prompt = self._get_prompts(datapoint)
            results = self._generate(prompt)
            out_data = {
                "post_id": datapoint["post_id"],
                "post": datapoint["post"]["text"],
                "response": results
            }
            torch.cuda.empty_cache()
            output_file.write(json.dumps(out_data) + "\n")
