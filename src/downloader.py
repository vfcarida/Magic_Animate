import os
import subprocess
import logging
from pathlib import Path
import typer
from .config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ModelDownloader:
    """Classe responsável pelo download de dependências e pesos de modelos."""
    
    def __init__(self):
        config.setup_directories()
        
    def clone_repo(self, repo_url: str, dest_dir: Path, use_lfs: bool = False, branch: str = None) -> bool:
        """Clona um repositório git caso ele ainda não exista no destino."""
        if dest_dir.exists() and any(dest_dir.iterdir()):
            logger.info(f"O repositório {dest_dir.name} já existe em {dest_dir}. Ignorando clone.")
            return True
            
        logger.info(f"Clonando repositório de {repo_url} para {dest_dir}...")
        
        cmd = ["git"]
        if use_lfs:
            cmd += ["lfs"]
            
        cmd += ["clone"]
        if branch:
            cmd += ["-b", branch]
            
        cmd += [repo_url, str(dest_dir)]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            logger.info(f"Repositório {dest_dir.name} clonado com sucesso.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Falha ao clonar {repo_url}. Erro: {e}")
            return False

    def download_densepose_weights(self) -> bool:
        """Baixa os pesos do DensePose via curl."""
        weights_dir = config.DENSEPOSE_DIR / "projects" / "DensePose"
        weights_dir.mkdir(parents=True, exist_ok=True)
        
        target_file = weights_dir / config.DENSEPOSE_WEIGHTS_NAME
        
        if target_file.exists():
            logger.info(f"Pesos do DensePose já existem em {target_file}. Ignorando download.")
            return True
            
        logger.info(f"Baixando pesos do DensePose de {config.DENSEPOSE_WEIGHTS_URL}...")
        cmd = ["curl", "-o", str(target_file), config.DENSEPOSE_WEIGHTS_URL]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            logger.info("Pesos do DensePose baixados com sucesso.")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Falha ao baixar pesos do DensePose. Erro: {e}")
            return False

    def run_all_downloads(self):
        """Executa todos os downloads necessários para o Magic Animate."""
        typer.echo(typer.style("Iniciando downloads de pesos e repositórios...", fg=typer.colors.BRIGHT_YELLOW))
        
        # 1. Detectron2 / DensePose (Apenas repositório base para acessar configs, instalação via pip ainda é recomendada)
        self.clone_repo(config.DENSEPOSE_REPO_URL, config.DENSEPOSE_DIR)
        
        # 2. Pesos do DensePose
        self.download_densepose_weights()
        
        # 3. Magic Animate
        self.clone_repo(config.MAGIC_ANIMATE_REPO_URL, config.MAGIC_ANIMATE_DIR)
        
        # 4. SD VAE
        sd_vae_dir = config.MAGIC_ANIMATE_DIR / "pretrained_models" / "sd-vae-ft-mse"
        self.clone_repo(config.SD_VAE_REPO, sd_vae_dir)
        
        # 5. Magic Animate Weights (usando LFS)
        ma_weights_dir = config.MAGIC_ANIMATE_DIR / "pretrained_models" / "MagicAnimate"
        self.clone_repo(config.MAGIC_ANIMATE_WEIGHTS_REPO, ma_weights_dir, use_lfs=True)
        
        # 6. Stable Diffusion v1-5
        sd_dir = config.MAGIC_ANIMATE_DIR / "pretrained_models" / "stable-diffusion-v1-5"
        self.clone_repo(config.STABLE_DIFFUSION_REPO, sd_dir, branch="fp16")
        
        typer.echo(typer.style("Todos os downloads essenciais foram finalizados! ✅", fg=typer.colors.GREEN))

if __name__ == "__main__":
    downloader = ModelDownloader()
    downloader.run_all_downloads()
