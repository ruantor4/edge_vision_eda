"""
plots.py

Geração de plots a partir do CSV agregado (section, metric, value).

Premissas:
- CSV no formato longo
- Sem criação de diretórios
- Apenas leitura e visualização
"""

from pathlib import Path
import logging
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

def plot_box_geometry_stats(csv_path: Path, output_path: Path) -> None:
    """
    Gera um gráfico de barras com estatísticas geométricas
    agregadas das bounding boxes.

    Métricas esperadas:
    - width_min, width_mean, width_max
    - height_min, height_mean, height_max
    - area_min, area_mean, area_max
    - proportion_min, proportion_mean, proportion_max
    """
    logger.info("Iniciando geração do plot de estatísticas geométricas das boxes")
    
    try:
        if not csv_path.exists():
            logger.error(f"O arquivo CSV não foi encontrado: {csv_path}")
            raise FileNotFoundError(csv_path)
        
        df = pd.read_csv(csv_path)
        
        expected_columns = {'section', 'metric', 'value'}

        if not expected_columns.issubset(set(df.columns)):
            logger.error(f"O CSV não contém as colunas esperadas: {expected_columns}")
            raise ValueError("Formato de CSV inválido")
        
        metrics_order: List[str] = [
            "width_min", "width_mean", "width_max",
            "height_min", "height_mean", "height_max",
            "area_min", "area_mean", "area_max",
            "proportion_min", "proportion_mean", "proportion_max",
        ]
        
        df_boxes = df[df["section"] == "boxes"].copy()

        missing_metrics = set(metrics_order) - set(df_boxes["metric"])
        if missing_metrics:
            logger.error(f"Métricas geométricas ausentes no CSV: {sorted(missing_metrics)}")
            raise ValueError("Métricas geométricas incompletas")
        
        df_boxes = (
            df_boxes[df_boxes["metric"].isin(metrics_order)]
                     .set_index("metric")
                     .loc[metrics_order]
                     .reset_index()
        )

        df_boxes["value"] = pd.to_numeric(df_boxes["value"], errors="raise")

        plt.figure(figsize=(12, 6))
        plt.bar(df_boxes["metric"], df_boxes["value"])
        plt.title("Estatísticas Geométricas das Bounding Boxes")
        plt.xlabel("Métrica")
        plt.ylabel("Valor normalizado")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        logger.info(f"Plot de estatísticas geométricas salvo em: {output_path}")
    
    except Exception as e:
        logger.error("Erro ao gerar plot de estatísticas geométricas das boxes", exc_info=e)
        raise

def plot_box_size_distribution(csv_path: Path, output_path: Path) -> None:
    """
    Gera um gráfico de barras com a distribuição agregada
    de tamanhos das bounding boxes.

    Métricas esperadas:
    - small
    - medium
    - large
    """
    logger.info("Iniciando geração do plot de distribuição de tamanhos das boxes")

    try:
        if not csv_path.exists():
            logger.error(f"CSV de métricas não encontrado: {csv_path}")
            raise FileNotFoundError(csv_path)
        
        df = pd.read_csv(csv_path)

        expected_sizes = ["small", "medium", "large"]
        df_sizes = df[df["section"] == "box_sizes"].copy()

        missing_sizes = set(expected_sizes) - set(df_sizes["metric"])
        if missing_sizes:
            logger.error(f"Métricas de tamanho ausentes no CSV: {sorted(missing_sizes)}")
            raise ValueError("Métricas de tamanho incompletas")
        
        # Ordem explicita para consistência analìtica
        df_sizes = (
            df_sizes.set_index("metric")
            .loc[expected_sizes]
            .reset_index()
        )

        df_sizes["value"] = pd.to_numeric(df_sizes["value"], errors="raise")

        plt.figure(figsize=(8, 5))
        plt.bar(df_sizes["metric"], df_sizes["value"])
        plt.title("Distribuição de Tamanhos das Bounding Boxes")
        plt.xlabel("Tamanho")
        plt.ylabel("Quantidade")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        logger.info(f"Plot de distribuição de tamanhos salvo em: {output_path}")

    except Exception as e:
        logger.error("Erro ao gerar plot de distribuição de tamanhos das boxes", exc_info=e)
        raise