"""
main.py

Ponto de entrada oficial do pipeline de EDA do projeto edge-vision-eda.

Responsabilidade:
- Orquestrar a execução do EDA de forma determinística
- Garantir preparação dos diretórios de artifacts
- Executar validação, métricas e plots na ordem correta

Este main NÃO realiza testes manuais nem validações exploratórias.
Ele assume que a configuração já foi validada previamente.
"""

import logging

from config.settings import (
    ARTIFACTS_PLOTS_DIR,
    DATASET_METRICS_PATH,
    ENABLE_PLOTS,
    ARTIFACTS_METRICS_DIR
    
)

from utils.logging_global import setup_logging
from core.validator import validate_dataset
from core.metrics import compute_dataset_metrics, save_metrics_csv
from viz.plots import plot_box_geometry_stats, plot_box_size_distribution

def main() -> None:
    """
    Executa o pipeline oficial de EDA.

    Etapas:
    1. Inicialização do logging
    2. Preparação de diretórios de artifacts
    3. Validação estrutural do dataset
    4. Cálculo e persistência de métricas
    5. Geração de plots (opcional)
    """

    # ETAPA 1 – LOGGING
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Iniciando pipeline oficial de EDA")
    

    # ETAPA 2 - DIRECTORIES
    try:
        logger.info("Garantindo diretórios de artifacts")

        ARTIFACTS_METRICS_DIR.mkdir(parents=True, exist_ok=True)
        ARTIFACTS_PLOTS_DIR.mkdir(parents=True, exist_ok=True)


        # ETAPA 3 - VALIDATION
        logger.info("Executando validação estrutural do dataset")
        
        validation_report = validate_dataset()
        
        for split, issues in validation_report.items():
    
            logger.info(
                    f"[{split}] labels sem imagem: {len(issues['labels_without_images'])} | "
                    f"imagens sem label: {len(issues['images_without_labels'])} | "
                    f"labels inválidos: {len(issues['invalid_labels'])}"
                )
        # ETAPA 4 - METRICS
        logger.info("Calculando e salvando métricas do dataset")

        metrics = compute_dataset_metrics()
        save_metrics_csv(metrics)

        logger.info(f"Métricas salvas em: {DATASET_METRICS_PATH}")

        # ETAPA 5 - PLOTS
        if ENABLE_PLOTS:
            logger.info("Gerando plots habilitada")

            plot_box_geometry_stats(
                csv_path=DATASET_METRICS_PATH,
                output_path=ARTIFACTS_PLOTS_DIR / "box_geometry_stats.png",
            )

            plot_box_size_distribution(
                csv_path=DATASET_METRICS_PATH,
                output_path=ARTIFACTS_PLOTS_DIR / "box_size_distribution.png",
            )

            logger.info("Plots do EDA gerados com sucesso")
        else:
            logger.info("Geração de plots desabilitada (ENABLE_PLOTS=False)")
        
        logger.info("Pipeline oficial de EDA concluído com sucesso.")
    
    except Exception as e:
        logger.error("Falha na execução do pipeline de EDA:", exc_info=e)
        raise

if __name__ == "__main__":
    main()