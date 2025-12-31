# Edge Vision EDA – Análise Exploratória de Dados para Visão Computacional

Aplicação desenvolvida em **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** para realizar **Análise Exploratória de Dados (EDA)** em datasets de **detecção de objetos**, como parte de uma **Prova de Conceito (PoC)** em **Visão Computacional**.

O projeto tem como objetivo analisar estruturalmente um **dataset externo**, identificar inconsistências, compreender a distribuição das **bounding boxes** e gerar **métricas e evidências visuais** que subsidiem decisões técnicas **antes da etapa de modelagem e treinamento de algoritmos**.

Este repositório é **exclusivamente analítico** e **não realiza treinamento, inferência ou normalização produtiva de dados**.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Objetivos do Projeto

- Realizar análise exploratória de datasets de detecção de objetos.
- Validar estruturalmente labels e bounding boxes.
- Identificar inconsistências, outliers e padrões nos dados.
- Gerar métricas estatísticas do dataset.
- Produzir visualizações para suporte à tomada de decisão.
- Garantir organização, rastreabilidade e reprodutibilidade do EDA.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Funcionalidades

| Categoria | Descrição |
|-----------|-----------|
| **Leitura de Dataset** | Consumo de dataset externo no formato de detecção de objetos. |
| **Validação Estrutural** | Verificação de labels inválidos, boxes fora de faixa e inconsistências. |
| **Análise Estatística** | Cálculo de métricas sobre dimensões e distribuição das bounding boxes. |
| **Visualizações (EDA)** | Geração de gráficos analíticos a partir de métricas agregadas do dataset. |
| **Persistência de Métricas** | Salvamento de métricas em formato CSV. |
| **Logs Estruturados** | Registro detalhado das etapas e resultados do EDA. |
| **Pipeline Reprodutível** | Execução controlada e determinística via `main.py`. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Tecnologias Utilizadas

| Categoria | Tecnologia |
|----------|------------|
| **Linguagem** | **[Python 3.11](https://docs.python.org/pt-br/3.11/contents.html)** |
| **Análise de Dados** | **[NumPy](https://numpy.org/doc/)** |
| **Visualização** | **[Matplotlib](https://matplotlib.org/stable/index.html)** |
| **Logging** | **[logging](https://docs.python.org/pt-br/3/library/logging.html)** |
| **Sistema** | **[pathlib](https://docs.python.org/pt-br/3/library/pathlib.html)**, **[csv](https://docs.python.org/pt-br/3/library/csv.html)**, **[statistics](https://docs.python.org/pt-br/3/library/statistics.html)** |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Estrutura de Diretórios

```bash
edge-vision-eda/
├── config/
│   └── settings.py                            # Configurações e paths do projeto
│
├── core/
│   ├── dataset_loader.py                      # Leitura do dataset externo
│   ├── metrics.py                             # Cálculo de métricas estatísticas agregadas
│   └── validator.py                           # Validação estrutural dos dados
│
├── viz/
│   └── plots.py                               # Geração de gráficos do EDA
│
├── artifacts/
│   ├── metrics/                               # CSVs de métricas
│   └── plots/                                 # Gráficos gerados
│
├── logs/
│   └── edge-vision-eda_2025-12-31.log
│
├── utils/
│   └── logging_global.py                      # Logging global do sistema
│
├── main.py                                    # Orquestração do pipeline de EDA 
│
├── documentação_técnica_edge-vision-eda.pdf   # Documentação Técnica
│
├── requirements.txt                           # Dependências
│
└── README.md                                  # Documentação
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Dataset

O dataset utilizado é **externo ao repositório** e não é versionado junto ao código.

Exemplo de organização no sistema:

```bash
edge-vision/
├── dataset_original/
│ ├── train/
│ ├── valid/
│ └── test/
└── edge-vision-eda/
```

O caminho para o dataset é configurado no arquivo:

```bash
config/settings.py
```

O projeto **apenas lê os dados**, não realizando qualquer modificação no dataset original.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Execução

### Passo 1 – Criar ambiente virtual
```bash
$ python -m venv .venv
$ source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
```

### Passo 2 – Instalar dependências
```bash
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

### Passo 3 – Executar o EDA
```bash
$ python main.py
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Observações Técnicas

- O projeto é focado exclusivamente em **EDA**.
- Não há qualquer etapa de treino ou inferência.
- O `main.py` atua apenas como orquestrador do fluxo.
- Os insumos gerados subsidiam o projeto **edge-vision-model**.