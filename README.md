# Magic Animate

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

O **Magic Animate** é um framework baseado em modelos de difusão projetado para criar vídeos a partir de imagens estáticas, aplicando uma sequência de movimento de referência extraída de outro vídeo. Diferente de outras soluções, o Magic Animate foca na consistência temporal extrema e na preservação fiel das características da imagem base.

Este projeto é focado na aplicação dessa tecnologia para animação de imagens de figuras humanas, permitindo recriar movimentos complexos para redes sociais, animações rápidas, entretenimento, e muito mais.

---

## 🏛 Arquitetura do Projeto

O repositório foi reestruturado usando as melhores práticas do mercado, orientadas a objetos, permitindo tanto o uso independente quanto como uma biblioteca integrada:

```text
Magic_Animate/
├── src/                        # Código-fonte e bibliotecas do motor
│   ├── config.py               # Central de variáveis e caminhos
│   ├── downloader.py           # Gestor de download de pesos
│   ├── pose_extractor.py       # Extração da máscara via DensePose
│   ├── animator.py             # Renderizador Magic Animate
│   └── pipeline.py             # CLI de Orquestração
├── notebooks/                  # Notebooks Jupyter para experimentação
├── tests/                      # Bateria de Testes Unitários
├── docs/                       # Guias e tutoriais
└── requirements.txt            # Dependências
```

---

## ⚙️ Pré-requisitos

Para garantir uma performance viável, os modelos requerem ambientes com aceleração por placa de vídeo dedicada (GPU).

- Python >= 3.8
- Placa de vídeo NVIDIA (CUDA habilitado recomendado > 16GB VRAM, ex. Google Colab T4/A100)
- `git` e `git-lfs` instalados no sistema.

## 🚀 Como Instalar

Siga os passos abaixo para preparar o seu ambiente local de desenvolvimento. Recomenda-se criar um ambiente virtual (venv, conda).

**1. Clone o repositório:**
```bash
git clone <url-deste-repositorio>
cd Magic_Animate
```

**2. Instale as dependências essenciais do Python:**
```bash
pip install -r requirements.txt
```

**3. Instale manualmente o detectron2 e magic-animate:**
Essas dependências são específicas e podem exigir compilação:
```bash
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
pip install 'git+https://github.com/hugozanini/magic-animate.git'
```

---

## 🛠 Como Usar

O projeto expõe um CLI orquestrado (Command Line Interface) na pasta `src/pipeline.py` para facilitar o uso.

Você pode rodar todo o fluxo de ponta a ponta informando um vídeo que contenha o movimento desejado e uma imagem estática que receberá a animação.

**Sintaxe de Uso:**
```bash
python -m src.pipeline --video "/caminho/para/video_referencia.mp4" --image "/caminho/para/imagem.jpg" --output "./outputs"
```

### O que acontece debaixo dos panos?
1. **Download Automático:** O sistema verificará se você possui todos os pesos das redes neurais necessários (DensePose, Stable Diffusion V1-5, SD-VAE). Caso não tenha, ele baixará automaticamente. Se quiser pular essa etapa, adicione a flag `--skip-download`.
2. **DensePose:** Processará o seu vídeo de referência e extrairá os movimentos usando a segmentação do Detectron2, gerando um `video_referencia_masked.mp4`.
3. **Magic Animate:** Fundo, rosto e proporções da sua imagem estática são fundidos com a máscara do vídeo via Diffusers e injetados em um processo de geração, salvando a saída na pasta `--output`.

### Notebook Interativo

Para exemplos interativos e testes manuais, visualize a demonstração que se encontra na pasta:
`notebooks/demo.ipynb`.

---

## 🤝 Guia de Contribuição

Contribuições são extremamente bem-vindas! Seja com relatórios de bugs, requests de features ou Pull Requests.

Leia o nosso [Guia de Contribuição](docs/CONTRIBUTING.md) detalhado para mais informações sobre as convenções do código e como rodar a bateria de testes.
