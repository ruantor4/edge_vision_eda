"""
dataset_loader.py

Responsável por percorrer o dataset externo e coletar
informações básicas sobre sua estrutura.

Este módulo:
- apenas lê o filesystem
"""

import logging
from typing import Dict

from config.settings import(
    DATASET_DIR, 
    DATASET_SPLITS, 
    IMAGES_DIRNAME, 
    LABELS_DIRNAME
)

logger = logging.getLogger(__name__)

def load_dataset_structure() -> Dict[str, Dict[str, int]]:
    """
    Percorre o dataset e coleta informações básicas por split.

    Retorna um dicionário simples:

    {
        "train": {
            "images": 120,
            "labels": 120
        },
        "valid": {
            "images": 30,
            "labels": 30
        }
    }

    Pastas ausentes são registradas em log,
    mas não interrompem a execução.
    """

    logger.info("Carregando estrutura do dataset...")
    dataset_info: Dict[str, Dict[str, int]] = {}

    # Percorremos cada split declarado no settings
    try:
        for split in DATASET_SPLITS:
            logger.info(f"Processando split: {split}")
            
            # Montamos os caminhos esperados
            images_path = DATASET_DIR / split / IMAGES_DIRNAME
            labels_path = DATASET_DIR / split / LABELS_DIRNAME

            # Verificamos se os diretórios existem
            if not images_path.exists():
                logger.warning(f"Pasta de imagens não encontrada: {images_path}")
            
            if not labels_path.exists():
                logger.warning(f"Pasta de labels não encontrada: {labels_path}")
            
            # Listamos os arquivos
            images = list(images_path.glob("*")) if images_path.exists() else []
            labels = list(labels_path.glob("*")) if labels_path.exists() else []

            # Guardamos apenas contagens
            dataset_info[split] = {
                "images": len(images),
                "labels": len(labels)
            }
    
            logger.info(
                "Split %s | imagens: %d | labels: %d",
                split,
                len(images),
                len(labels),
            )
    except Exception as e:
        logger.error("Erro ao carregar estrutura do dataset:", exc_info=e)
        raise

    logger.info("Leitura da estrutura do dataset finalizada")
    return dataset_info