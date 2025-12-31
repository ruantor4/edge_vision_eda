"""
logging_global.py

Responsável por configurar o sistema de logging do projeto.

Este módulo:
- cria um logger global
- define formato de log
- define arquivo de saída
"""
from datetime import datetime
import logging

from config.settings import LOGS_DIR

def setup_logging() -> None:
    """
    Configura o sistema de logging do projeto.

    Esta função deve ser chamada UMA VEZ no início do main.
    Depois disso, qualquer módulo pode usar logging.getLogger().
    """

    # Garante que o diretório de logs exista
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Data atual para o nome do arquivo de log
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Arquivo de log com data
    log_file = LOGS_DIR / f"edge-vision-eda_{date_str}.log"
    
    # Formato do log:
    log_format = "%(asctime)s | %(levelname)s | %(message)s"

    logging.basicConfig(
        level = logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],

    )