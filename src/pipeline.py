import typer
from pathlib import Path
from src.downloader import ModelDownloader
from src.pose_extractor import PoseExtractor
from src.animator import Animator

app = typer.Typer(help="Pipeline de Animação - Magic Animate")

@app.command()
def run_pipeline(
    input_video: str = typer.Option(..., "--video", "-v", help="Caminho do vídeo de movimento de entrada (referência de pose)."),
    input_image: str = typer.Option(..., "--image", "-i", help="Caminho da imagem que será animada."),
    output_dir: str = typer.Option(None, "--output", "-o", help="Diretório de saída (Opcional, padrão é ./outputs)."),
    skip_download: bool = typer.Option(False, "--skip-download", help="Pula a verificação e o download dos modelos/repositórios."),
    seed: int = typer.Option(2, "--seed", help="Semente para reprodutibilidade."),
    steps: int = typer.Option(35, "--steps", help="Número de passos de inferência."),
    guidance_scale: float = typer.Option(7.5, "--guidance", help="Guidance scale do modelo.")
):
    """Executa a pipeline completa: Download (opcional) -> Extração de Poses -> Geração da Animação."""
    typer.echo(typer.style("🚀 Iniciando Pipeline do Magic Animate...", fg=typer.colors.MAGENTA, bold=True))

    if not skip_download:
        typer.echo("Verificando e baixando dependências necessárias...")
        downloader = ModelDownloader()
        downloader.run_all_downloads()
    
    typer.echo(typer.style("\n--- Passo 1: Extração de Poses (DensePose) ---", fg=typer.colors.BLUE))
    extractor = PoseExtractor()
    masked_video_path = extractor.extract_poses(input_video)
    
    typer.echo(typer.style("\n--- Passo 2: Geração da Animação ---", fg=typer.colors.BLUE))
    animator = Animator()
    animator.animate(
        reference_image_path=input_image,
        motion_sequence_path=masked_video_path,
        seed=seed,
        steps=steps,
        guidance_scale=guidance_scale,
        output_dir=output_dir
    )
    
    typer.echo(typer.style("\n🎉 Pipeline executada com sucesso!", fg=typer.colors.GREEN, bold=True))

if __name__ == "__main__":
    app()
