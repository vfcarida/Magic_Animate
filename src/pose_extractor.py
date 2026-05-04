import sys
import os
import cv2
import torch
import numpy as np
import logging
from pathlib import Path
from tqdm import tqdm
import typer

from .config import config

logger = logging.getLogger(__name__)

class PoseExtractor:
    """Extração de poses (DensePose) de vídeos usando detectron2."""

    def __init__(self):
        self._setup_densepose_path()
        try:
            from detectron2.engine.defaults import DefaultPredictor
            from densepose.vis.extractor import DensePoseResultExtractor
            from densepose.structures import DensePoseDataRelative
            from densepose.vis.base import MatrixVisualizer
            from apply_net import DumpAction, create_argument_parser
            
            self.DefaultPredictor = DefaultPredictor
            self.DensePoseResultExtractor = DensePoseResultExtractor
            self.DensePoseDataRelative = DensePoseDataRelative
            self.MatrixVisualizer = MatrixVisualizer
            self.DumpAction = DumpAction
            self.create_argument_parser = create_argument_parser
        except ImportError as e:
            logger.error("Detectron2 ou DensePose não encontrados. Instale as dependências corretamente.")
            raise e

    def _setup_densepose_path(self):
        """Adiciona o diretório DensePose do repositório detectron2 ao sys.path para importações."""
        dp_path = config.DENSEPOSE_DIR / "projects" / "DensePose"
        if not dp_path.exists():
            raise FileNotFoundError(f"Diretório DensePose não encontrado em {dp_path}. Execute o downloader primeiro.")
        if str(dp_path) not in sys.path:
            sys.path.append(str(dp_path))

    def extract_poses(self, input_video: str, output_video: str = None) -> str:
        """Processa um vídeo e gera as máscaras de segmentação do DensePose."""
        if not output_video:
            out_path = Path(input_video)
            output_video = str(out_path.parent / f"{out_path.stem}_masked.mp4")

        typer.echo(typer.style(f"Iniciando extração de DensePose para: {input_video}", fg=typer.colors.BRIGHT_YELLOW))
        
        cfg_path = str(config.DENSEPOSE_DIR / "projects" / "DensePose" / config.DENSEPOSE_CONFIG_YAML)
        model_path = str(config.DENSEPOSE_DIR / "projects" / "DensePose" / config.DENSEPOSE_WEIGHTS_NAME)

        parser = self.create_argument_parser()
        args = parser.parse_args(args=[
            "dump",
            cfg_path,
            model_path,
            "input.jpg",  # Placeholder required by apply_net
            "--output",
            "dump.pkl"
        ])

        opts = []
        cfg = self.DumpAction.setup_config(args.cfg, args.model, args, opts)
        predictor = self.DefaultPredictor(cfg)

        cap = cv2.VideoCapture(input_video)
        if not cap.isOpened():
            logger.error(f"Não foi possível abrir o vídeo: {input_video}")
            raise ValueError(f"Não foi possível abrir o vídeo: {input_video}")

        img_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        img_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        img_size = 512  # Tamanho de entrada do Magic Animate
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_video, fourcc, fps, (img_size, img_size))

        val_scale = 255.0 / self.DensePoseDataRelative.N_PART_LABELS
        mask_visualizer = self.MatrixVisualizer(
            inplace=True, cmap=cv2.COLORMAP_VIRIDIS, val_scale=val_scale, alpha=1.0
        )

        extractor = self.DensePoseResultExtractor()

        typer.echo(typer.style("Processando frames...", fg=typer.colors.CYAN))
        
        with tqdm(total=total_frame_count, position=0, leave=True) as pbar:
            while True:
                ret, img = cap.read()
                if not ret:
                    break

                with torch.no_grad():
                    outputs = predictor(img)["instances"].to("cpu")

                data = extractor(outputs)
                densepose_result, boxes_xywh = data

                matrix_scaled_8u = np.zeros((img_height, img_width), dtype=np.uint8)
                matrix_vis = cv2.applyColorMap(matrix_scaled_8u, cv2.COLORMAP_VIRIDIS)

                for i, result in enumerate(densepose_result):
                    iuv_array = torch.cat(
                        (result.labels[None].type(torch.float32), result.uv * 255.0)
                    ).cpu().type(torch.uint8).cpu().numpy()

                    bbox_xywh = boxes_xywh.cpu().numpy()[0]
                    
                    def _extract_i_from_iuvarr(iuv_arr):
                        return iuv_arr[0, :, :]

                    matrix = _extract_i_from_iuvarr(iuv_array)
                    segm = _extract_i_from_iuvarr(iuv_array)
                    mask = np.zeros(matrix.shape, dtype=np.uint8)
                    mask[segm >= 0] = 1

                    mask_visualizer.visualize(matrix_vis, mask, matrix, bbox_xywh)
                    # Quebrar loop no primeiro humano detectado para evitar múltiplas poses
                    break

                # Padding para manter as proporções do frame
                height, width = matrix_vis.shape[:2]
                if height > width:
                    pad = (height - width) // 2
                    matrix_vis = np.pad(matrix_vis, ((0, 0), (pad, pad), (0, 0)), 'edge')
                elif width > height:
                    pad = (width - height) // 2
                    matrix_vis = np.pad(matrix_vis, ((pad, pad), (0, 0), (0, 0)), 'edge')

                matrix_vis = cv2.resize(matrix_vis, (img_size, img_size), cv2.INTER_NEAREST)
                writer.write(matrix_vis)
                pbar.update(1)

        writer.release()
        cap.release()
        
        typer.echo(typer.style(f"Máscara DensePose salva em: {output_video} ✅", fg=typer.colors.GREEN))
        return output_video
