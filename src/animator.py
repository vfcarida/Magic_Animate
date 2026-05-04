import sys
import numpy as np
import logging
from PIL import Image
from pathlib import Path
import typer

from .config import config

logger = logging.getLogger(__name__)

class Animator:
    """Classe responsável por integrar e executar a animação com o Magic Animate."""

    def __init__(self):
        self._setup_magic_animate_path()
        try:
            from demo.animate import MagicAnimate
            self.MagicAnimate = MagicAnimate
            # Instanciar apenas sob demanda para não estourar a memória se instanciar a classe e não usar
            self.animator = None
        except ImportError as e:
            logger.error("Magic Animate não encontrado. Verifique se as dependências foram instaladas e os diretórios estão corretos.")
            raise e

    def _setup_magic_animate_path(self):
        """Adiciona o diretório do Magic Animate ao sys.path para importações."""
        ma_path = config.MAGIC_ANIMATE_DIR
        if not ma_path.exists():
            raise FileNotFoundError(f"Diretório Magic Animate não encontrado em {ma_path}. Execute o downloader primeiro.")
        
        if str(ma_path) not in sys.path:
            sys.path.insert(0, str(ma_path))

    def read_image(self, image_path: str, size: int = 512) -> np.ndarray:
        """Lê e redimensiona a imagem de referência."""
        try:
            image = Image.open(image_path)
            return np.array(image.resize((size, size)))
        except Exception as e:
            logger.error(f"Erro ao ler imagem {image_path}: {e}")
            raise e

    def animate(self, reference_image_path: str, motion_sequence_path: str, 
                seed: int = 2, steps: int = 35, guidance_scale: float = 7.5, 
                output_dir: str = None) -> str:
        """Executa a geração da animação combinando a imagem e a sequência de movimento."""
        
        if not output_dir:
            output_dir = str(config.OUTPUT_DIR)
            
        typer.echo(typer.style("Inicializando Magic Animate...", fg=typer.colors.CYAN))
        
        if not self.animator:
            self.animator = self.MagicAnimate()
            
        reference_image = self.read_image(reference_image_path)
        
        typer.echo(typer.style("Gerando vídeo animado... Isso pode demorar.", fg=typer.colors.BRIGHT_YELLOW))
        
        try:
            # O magic animate salva o vídeo no output_dir fornecido internamente
            animation_path = self.animator(
                reference_image, 
                motion_sequence_path, 
                seed, 
                steps, 
                guidance_scale, 
                output_dir
            )
            typer.echo(typer.style(f"Animação concluída! Verifique o diretório: {output_dir} ✅", fg=typer.colors.GREEN))
            return animation_path
        except Exception as e:
            logger.error(f"Falha ao gerar animação: {e}")
            raise e
