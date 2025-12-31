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
from config.settings import DATASET_DIR, DATASET_SPLITS, IMAGES_DIRNAME, LABELS_DIRNAME, ROOT_DIR
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
    setup_logging()

    logger = logging.getLogger(__name__)
    
    logger.info("Iniciando edge-vision-eda")
    logger.info("Testando configuração inicial")
    

    # TESTE 1 – Verificar se o ROOT_DIR está correto
    logger.info(f"ROOT_DIR: {ROOT_DIR}")


    # TESTE 2 – Verificar se o DATASET_DIR existe
    logger.info(f"DATASET_DIR: {DATASET_DIR}")
    logger.info(f"DATASET_DIR existe? {DATASET_DIR.exists()}")

    logger.info("Teste finalizado.")

    # TESTE 3 – Verificar estrutura do dataset por split
    """
    DATASET_SPLITS é uma tupla com os nomes esperados:
    ("train", "valid", "test")
    
    Para cada split, verificamos se existem:
    - pasta images/
    - pasta labels/
    """
    for split in DATASET_SPLITS:
        print(f"SPLIT: {split}")
        
        # Caminho da pasta de imagens
        images_path = DATASET_DIR / split / IMAGES_DIRNAME

        # Caminho da pasta de labels
        labels_path = DATASET_DIR / split / LABELS_DIRNAME

        # Verificamos se essas pastas existem no sistema
        print("  Images path:", images_path)
        print("  Existe?", images_path.exists())

        print("  Labels path:", labels_path)
        print("  Existe?", labels_path.exists())

        print("-" * 50)


if __name__ == "__main__":
    """
    Esta condição verifica se o arquivo main.py está sendo executado
    diretamente (python main.py) ou se está sendo importado como um módulo
    em outro arquivo.

    Se estiver sendo executado diretamente, chamamos a função main().
    """
    main()
