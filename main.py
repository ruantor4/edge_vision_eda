"""
main.py

Este arquivo é o ponto de entrada do projeto.

Neste momento do desenvolvimento, o main.py serve apenas para:
- testar se o settings.py está funcionando
- entender se os paths estão corretos
- garantir que o dataset pode ser acessado

Este main NÃO é o pipeline final.
Ele é apenas um teste inicial para validar configuração.
"""

import logging
from core.metrics import compute_dataset_metrics, save_metrics_csv
from core.validator import validate_dataset
from config.settings import (
    ROOT_DIR,
    DATASET_DIR,
    DATASET_SPLITS,
    IMAGES_DIRNAME,
    LABELS_DIRNAME,
    ARTIFACTS_METRICS_DIR
)

from utils.logging_global import setup_logging

def main() -> None:
    """
    Função principal do programa.

    Em Python, é uma boa prática colocar o código principal
    dentro de uma função chamada main(), em vez de escrever
    tudo solto no arquivo.

    Isso facilita:
    - leitura
    - testes
    - refatoração depois
    """

    # ETAPA 0 – Inicializar logging
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
    
        logger.info("Iniciando edge-vision-eda")
        logger.info("Testando configuração inicial")
    
    except Exception as e:
        print("Erro ao configurar o logging:", e)
        return

    # TESTE 1 – Verificar se o ROOT_DIR está correto
    try:
        logger.info(f"ROOT_DIR: {ROOT_DIR}")

    except Exception as e:
        logger.error("Erro ao acessar ROOT_DIR:", exc_info=e)
        return


    # TESTE 2 – Verificar se o DATASET_DIR existe
    try:
        logger.info(f"DATASET_DIR: {DATASET_DIR}")
        logger.info(f"DATASET_DIR existe? {DATASET_DIR.exists()}")

        logger.info("Teste finalizado.")

    except Exception as e:
        logger.error("Erro ao acessar DATASET_DIR:", exc_info=e)
        return

    # TESTE 3 – Verificar estrutura do dataset por split
    """
    DATASET_SPLITS é uma tupla com os nomes esperados:
    ("train", "valid", "test")
    
    Para cada split, verificamos se existem:
    - pasta images/
    - pasta labels/
    """
    try:
        for split in DATASET_SPLITS:
            print(f"SPLIT: {split}")
            
            # Caminho da pasta de imagens
            images_dir = DATASET_DIR / split / IMAGES_DIRNAME

            # Caminho da pasta de labels
            labels_dir = DATASET_DIR / split / LABELS_DIRNAME

            # Verificamos se essas pastas existem no sistema
            if not images_dir.exists():
                logger.warning(f"Pasta de imagens não encontrada: {images_dir}")
            
            if not labels_dir.exists():
                logger.warning(f"Pasta de labels não encontrada: {labels_dir}")

    except Exception as e:
        logger.error("Erro ao verificar estrutura do dataset por split:", exc_info=e)
        return
    
    # TESTE 4 – Validar dataset (validator)
    try:
        logger.info("Iniciando validação do dataset")
        
        validation_report = validate_dataset()

        for split, issues in validation_report.items():
            logger.info(f"Resumo do split: {split}")
            logger.info(
                f" Imagens negativas (sem label): {len(issues['images_without_labels'])}"
            )
            logger.info(
                f" Labels inválidos: {len(issues['invalid_labels'])}"
            )
    

    except Exception as e:
        logger.error("Erro ao validar o dataset:", exc_info=e)
        return
    
    # TESTE 5 – Preparar diretório de métricas
    try:
        logger.info("Garantindo diretório de métricas")
        ARTIFACTS_METRICS_DIR.mkdir(parents=True, exist_ok=True)

    except Exception as e:
        logger.error("Erro ao criar diretório de métricas", exc_info=e)
        return
    
    # TESTE 6 – Calcular e salvar métricas do dataset
    try:
        logger.info("Calculando métricas exploratórias do dataset")

        metrics = compute_dataset_metrics()
        save_metrics_csv(metrics)

        logger.info("Métricas calculadas e salvas em CSV.")

    except Exception as e:
        logger.error("Erro ao calcular ou salvar métricas do dataset:", exc_info=e)
        return
    
    logger.info("Todos os testes concluídos com sucesso.")

if __name__ == "__main__":
    """
    Este bloco garante que a função main() só seja executada
    quando este arquivo for rodado diretamente.
    """
    main()
