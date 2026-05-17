import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt_BR')

quantidade_lancamentos = 100000

historicos = [
    "Recebimento Juros",
    "Pagamento Fornecedor",
    "Estorno Pagto NF",
    "Tarifa Bancária",
    "Transferência Tesouraria",
    "Apropriação Receita",
    "Baixa Duplicata",
    "ISS Retido",
    "PIS COFINS",
    "Pagamento Folha"
]

usuarios = [
    "Lucas Ferreira Rataczyk",
    "Grace Maciel Rocha",
    "Rita Maria Araújo Da Silva",
    "Tiago Oliveira",
    "Carlos Henrique"
]

origens = [
    "Tesouraria - Movimentos",
    "Financeiro",
    "Fiscal",
    "Contabilidade",
    "Folha de Pagamento"
]

dados = []

for i in range(quantidade_lancamentos):

    debito = round(random.uniform(10, 50000), 2)
    credito = 0

    if random.choice([True, False]):
        credito = debito
        debito = 0

    linha = {
        "empresa": random.randint(1, 30),
        "conta_contabil": random.randint(10000, 99999),
        "data_lancamento": fake.date_between(start_date='-1y', end_date='today'),
        "lote": random.randint(1000, 9999),
        "documento_seq": random.randint(1000000000, 9999999999),
        "historico": random.choice(historicos),
        "debito": debito,
        "credito": credito,
        "fornecedor": random.randint(1000, 9999),
        "conta_financeira": random.randint(100, 999),
        "projeto": random.randint(1, 50),
        "centro_custo": f"M{random.randint(10000,99999)}",
        "origem": random.choice(origens),
        "codigo_usuario": random.randint(100, 999),
        "usuario_lote": random.choice(usuarios),
        "data_lote": fake.date_time_this_year()
    }

    dados.append(linha)

df = pd.DataFrame(dados)

df.to_excel(
    "data/lancamentos_contabeis_fake.xlsx",
    index=False
)

print("Dataset gerado com sucesso!")