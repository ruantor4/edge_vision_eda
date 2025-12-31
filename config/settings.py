"""
settings.py

Arquivo de configuração central do projeto edge-vision-eda.

Responsabilidades:
- Definir paths do projeto
- Declarar estrutura esperada do dataset (somente leitura)
- Centralizar parâmetros analíticos do EDA
"""

from pathlib import Path


# ROOT DO PROJETO
ROOT_DIR = Path(__file__).resolve().parent.parent


# DATASET EXTERNO
DATASET_DIR = ROOT_DIR.parent / "dataset_original"


# SPLITS DO DATASET
DATASET_SPLITS = ("train", "valid", "test")


# ESTURUTURA DO DATASET
IMAGES_DIRNAME = "images"
LABELS_DIRNAME = "labels"


# ARTIFACTS GERADOS PELO EDA
ARTIFACTS_DIR = ROOT_DIR / "artifacts"

ARTIFACTS_EDA_DIR = ARTIFACTS_DIR / "eda"
ARTIFACTS_METRICS_DIR = ARTIFACTS_DIR / "metrics"
ARTIFACTS_PLOTS_DIR = ARTIFACTS_DIR / "plots"


# LOGS
LOGS_DIR = ROOT_DIR / "logs"


# PARÂMETROS ANALÍTICOS DO EDA

# Número de bins para histogramas
HISTOGRAM_BINS = 50

# Percentis usados para análise de outliers
OUTLIER_PERCENTILES = (1, 99)

# Flag para ativar/desativar geração de plots
ENABLE_PLOTS = True


