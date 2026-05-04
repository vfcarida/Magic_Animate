import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    """Configurações globais e definições de caminhos do projeto."""
    
    # Diretórios Base
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODELS_DIR: Path = BASE_DIR / "pretrained_models"
    OUTPUT_DIR: Path = BASE_DIR / "outputs"
    
    # Detalhes do DensePose
    DENSEPOSE_REPO_URL: str = "https://github.com/facebookresearch/detectron2"
    DENSEPOSE_DIR: Path = BASE_DIR / "detectron2"
    DENSEPOSE_WEIGHTS_URL: str = "https://dl.fbaipublicfiles.com/densepose/densepose_rcnn_R_50_FPN_s1x/165712039/model_final_162be9.pkl"
    DENSEPOSE_CONFIG_YAML: str = "configs/densepose_rcnn_R_50_FPN_s1x.yaml"
    DENSEPOSE_WEIGHTS_NAME: str = "model_final_162be9.pkl"
    
    # Detalhes do Magic Animate
    MAGIC_ANIMATE_REPO_URL: str = "https://github.com/hugozanini/magic-animate.git"
    MAGIC_ANIMATE_DIR: Path = BASE_DIR / "magic-animate"
    
    # Repositórios do HuggingFace
    SD_VAE_REPO: str = "https://huggingface.co/stabilityai/sd-vae-ft-mse"
    MAGIC_ANIMATE_WEIGHTS_REPO: str = "https://huggingface.co/zcxu-eric/MagicAnimate"
    STABLE_DIFFUSION_REPO: str = "https://huggingface.co/runwayml/stable-diffusion-v1-5"
    
    @classmethod
    def setup_directories(cls):
        """Garante que os diretórios necessários existem."""
        cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
config = Config()
