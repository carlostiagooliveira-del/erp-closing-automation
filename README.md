# 🏦 ERP Closing Automation

## O que é

Pipeline completo de automação de fechamento contábil com geração
de dataset, validação de lançamentos e dashboard interativo.

## Por que fiz

Trabalhei 10 anos em controladoria executando fechamentos mensais
manualmente. Esse projeto automatiza as etapas mais repetitivas
do processo usando Python.

## Tecnologias

- Python 3.x
- Pandas
- OpenPyXL
- Streamlit
- Plotly

## Como rodar
pip install -r requirements.txt
python main.py

## Funcionalidades

- Geração de 100.000 lançamentos contábeis simulados com valores realistas
- 7 validações contábeis automatizadas (débitos/créditos, datas, duplicatas, suspeitos)
- Relatório de validação exportado em `.txt`
- Dashboard interativo com KPIs, gráficos e tabela de inconsistências

## Estrutura
├── dashboard/        # Dashboard Streamlit
├── data/             # Dataset gerado (ignorado pelo git)
├── reports/          # Relatórios gerados (ignorado pelo git)
├── src/
│   ├── generate_dataset.py   # Geração dos lançamentos
│   └── validate_entries.py   # Validações contábeis
└── main.py           # Orquestrador com menu interativo