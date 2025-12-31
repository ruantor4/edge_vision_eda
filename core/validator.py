"""
validator.py

Responsável por validar a consistência entre imagens e labels
no dataset utilizado para EDA.

Este módulo identifica problemas comuns como:
- labels sem imagem correspondente
- imagens sem label
- labels mal formatados
"""

from ast import Dict, Set
import logging
from pathlib import Path
from typing import Dict, List, Set

from config.settings import (
    DATASET_DIR, 
    DATASET_SPLITS, 
    IMAGES_DIRNAME, 
    LABELS_DIRNAME
)

logger = logging.getLogger(__name__)

def validade_dataset() -> Dict[str, Dict[str, List[str]]]:
    """
    Valida a consistência do dataset por split.

    Retorna um dicionário no formato:

    {
        "train": {
            "labels_without_images": [...],
            "images_without_labels": [...],
            "invalid_labels": [...]
        }
    }
    """

    logger.info("Iniciando validação do dataset...")

    validade_report: Dict[str, Dict[str, List[str]]] = {}

    # Percorre cada split definido no settings
    for split in DATASET_SPLITS:
        logger.info(f"Validando split: {split}")
        
        images_dir = DATASET_DIR / split / IMAGES_DIRNAME
        labels_dir = DATASET_DIR / split / LABELS_DIRNAME

        images = {img.stem for img in images_dir.glob("*")} if images_dir.exists() else set()
        labels = {lbl.stem for lbl in labels_dir.glob("*")} if labels_dir.exists() else set()

        # Coleta nomes base
        images: Set[str] = (
            {img.stem for img in images_dir.glob("*")} 
            if images_dir.exists() 
            else set()
        )
        labels: Set[str] = (
            {lbl.stem for lbl in labels_dir.glob("*")} 
            if labels_dir.exists() 
            else set()
        )

        # ERRO: label existe, mas imagem não
        labels_without_images = sorted(labels - images)


        # IMAGENS NEGATIVAS: imagem existe, mas label não
        images_without_labels = sorted(images - labels)

        invalid_labels: List[str] = []
        
        # Validação básica do conteúdo dos arquivos de label
        if labels_dir.exists():
            for label_file in labels_dir.glob("*.txt"):
                try:
                    content = label_file.read_text().strip()

                    # ERRO: arquivo de label vazio
                    if not content:
                        logger.warning(f"Label vazio: {label_file}")
                        invalid_labels.append(label_file.name)
                        continue

                    # Cada linha deve conter exatamente 5 valores padrão YOLO
                    for line in content.splitlines():
                        parts = line.split()

                        if len(parts) != 5:
                            logger.warning(f"Label mal formatado em {label_file}: {line}")
                            invalid_labels.append(label_file.name)
                            break

                except Exception as e:
                    # Exceção aqui significa dado inválido, não falha do sistema
                    logger.error(f"Erro ao ler label {label_file}: {e}")
                    invalid_labels.append(label_file.name)
        
        
        validade_report[split] = {
            "labels_without_images": labels_without_images,
            "images_without_labels": images_without_labels,
            "invalid_labels": invalid_labels,
        }

        logger.info(
            "Split %s | labels sem imagem: %d | imagens sem label: %d | labels inválidos: %d",
            split,
            len(labels_without_images),
            len(images_without_labels),
            len(invalid_labels),
        )

    logger.info("Validação do dataset concluída.")
    return validade_report