import hydra
from omegaconf import DictConfig

from src.response_generation import load_dataset, ResponseGenerator

@hydra.main(version_base=None, config_path="configs", config_name="llama8b")
def generation(cfg: DictConfig):

    dataset = load_dataset(cfg)
    generator = ResponseGenerator(cfg)
    generator.load_model()
    print("Model loaded")
    generator.generate_response(dataset)


if __name__ == '__main__':
    generation()