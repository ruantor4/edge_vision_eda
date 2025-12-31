"""
metrics.py

Responsável por calcular métricas estatísticas do dataset
para fins de Análise Exploratória de Dados (EDA).

Este módulo:
- considera apenas labels válidos
- ignora labels vazios (imagens negativas)
- ignora labels inválidos

Gera métricas agregadas para posterior salvamento em CSV.
"""

import csv
import logging
from statistics import mean
from typing import List, Set, Tuple

from config.settings import (
    ARTIFACTS_METRICS_DIR, 
    DATASET_DIR, 
    DATASET_SPLITS, 
    LABELS_DIRNAME
) 

logger = logging.getLogger(__name__)

# FUNÇÃO AUXILIAR
def _classify_box(area: float) -> str:
    """
    Classifica bounding box em small / medium / large
    baseado na área normalizada (YOLO-style).
    """

    if area < 0.02:
        return "small"
    
    elif area < 0.15:
        return "medium"
    
    else:
        return "large"
    

# CALCULO DE MÉTRICAS
def compute_dataset_metrics() -> List[Tuple[str, str, object]]:
    """
    Calcula métricas exploratórias do dataset.

    Retorna uma lista de tuplas no formato:
    (section, metric, value)

    Formato para salvar em CSV.
    """ 

    logger.info("Iniciando cálculo de métricas do dataset...")

    # Inicialização dos acumuladores
    widths: List[float] = []
    heights: List[float] = []
    areas: List[float] = []
    proportions: List[float] = []
    classes: Set[float] = set()

    # contador de tamanhos
    box_sizes = {
        "small": 0,
        "medium": 0,
        "large": 0
    }

    images_with_objects: Set[str] = set()
    total_boxes = 0
    
    try:
        # Percorre cada split definido no settings
        for split in DATASET_SPLITS:
            labels_dir = DATASET_DIR / split / LABELS_DIRNAME

            if not labels_dir.exists():
                logger.warning(f"Pasta de labels não encontrada: {labels_dir}")
                continue

            for label_file in labels_dir.glob("*.txt"):
                try:
                    with open(label_file, "r") as f:
                        content = f.read().strip()
                    
                except Exception as e:
                    logger.warning(f"Não foi possível ler o arquivo {label_file}: {e}")
                    continue
                    
                # label vazio = negativo
                if not content:
                    continue  
                        
                images_with_objects.add(label_file.stem)

                for line in content.splitlines():
                    parts = line.split()
                        
                    # label inválido   
                    if len(parts) != 5:
                        logger.warning(f"Label mal formatado em {label_file}: {line}")
                        continue  

                    try:
                        cls, _,_, w, h = parts
                        w = float(w)
                        h = float(h)
                    
                    except ValueError as exc:
                        logger.warning(f"Erro ao converter valores numéricos em {label_file}: {exc}")
                        continue  # label inválido

                    area = w * h
                    proportion = w / h if h > 0 else 0.0

                    widths.append(w)
                    heights.append(h)
                    areas.append(area)
                    proportions.append(proportion)
                    classes.add(float(cls))

                    box_sizes[_classify_box(area)] += 1
                    total_boxes += 1
    
    except Exception as e:
        logger.error("Erro ao calcular métricas do dataset:", exc_info=e)
        raise
    
    
    metrics: List[Tuple[str, str, object]] = []

    if total_boxes == 0:
        logger.error("Nenhuma bounding box válida encontrada no dataset.")
        return metrics
    
    try:
        metrics.extend([
            ("labels", "images_with_objects", len(images_with_objects)),
            ("labels", "total_boxes", total_boxes),
            ("labels", "classes", sorted(classes)),

            ("boxes", "width_mean", mean(widths)),
            ("boxes", "width_min", min(widths)),
            ("boxes", "width_max", max(widths)),

            ("boxes", "height_mean", mean(heights)),
            ("boxes", "height_min", min(heights)),
            ("boxes", "height_max", max(heights)),

            ("boxes", "area_mean", mean(areas)),
            ("boxes", "area_min", min(areas)),
            ("boxes", "area_max", max(areas)),

            ("boxes", "proportion_mean", mean(proportions)),
            ("boxes", "proportion_min", min(proportions)),
            ("boxes", "proportion_max", max(proportions)),
        ])

        for size, count in box_sizes.items():
            metrics.append(("box_sizes", size, count))

    except Exception as e:
        logger.error("Erro ao calcular estatísticas do dataset:", exc_info=e)
        raise

    logger.info("Cálculo de métricas do dataset concluído.")
    return metrics

def save_metrics_csv(metrics: List[Tuple[str, str, object]]) -> None:
    """
    Salva métricas em CSV dentro de artifacts/metrics.

    Assume que o diretório já existe.
    """
    output_path = ARTIFACTS_METRICS_DIR / "dataset_metrics.csv"

    try:
        with open(output_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["section", "metric", "value"])

            for section, metric, value in metrics:
                writer.writerow([section, metric, value])
        
        logger.info(f"Métricas salvas em CSV: {output_path}")

    except Exception as e:
        logger.error("Erro ao salvar métricas em CSV:", exc_info=e)
        raise    

                    
        