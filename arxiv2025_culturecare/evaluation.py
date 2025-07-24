import hydra
from omegaconf import DictConfig

from src.geval import load_dataset, GEvaluator

@hydra.main(version_base=None, config_path="configs", config_name="judge_qwen72b")
def evaluation(cfg: DictConfig):
    dataset = load_dataset(cfg)
    evaluator = GEvaluator(cfg)
    if "gpt" in cfg.model_name:
        evaluator.load_gpt_model()
    else:
        evaluator.load_model()
    print("Model loaded")
    evaluator.evaluate_responses(dataset)


if __name__ == '__main__':
    evaluation()
