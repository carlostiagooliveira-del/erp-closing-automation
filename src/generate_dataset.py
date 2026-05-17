import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt_BR')

quantidade_lancamentos = 100000

# Faixas de valor realistas por tipo de lançamento
faixas_por_historico = {
    "Tarifa Bancária":           (5,     150),
    "ISS Retido":                (50,    800),
    "PIS COFINS":                (100,   3000),
    "Pagamento Folha":           (1500,  8000),
    "Pagamento Fornecedor":      (500,   15000),
    "Estorno Pagto NF":          (200,   10000),
    "Recebimento Juros":         (50,    3000),
    "Transferência Tesouraria":  (5000,  50000),
    "Apropriação Receita":       (1000,  20000),
    "Baixa Duplicata":           (300,   8000),
}

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
    historico = random.choice(list(faixas_por_historico.keys()))
    minimo, maximo = faixas_por_historico[historico]
    valor = round(random.uniform(minimo, maximo), 2)

    debito  = valor
    credito = 0

    if random.choice([True, False]):
        credito = valor
        debito  = 0

    linha = {
        "empresa":         random.randint(1, 30),
        "conta_contabil":  random.randint(10000, 99999),
        "data_lancamento": fake.date_between(start_date='-1y', end_date='today'),
        "lote":            random.randint(1000, 9999),
        "documento_seq":   random.randint(1000000000, 9999999999),
        "historico":       historico,
        "debito":          debito,
        "credito":         credito,
        "fornecedor":      random.randint(1000, 9999),
        "conta_financeira":random.randint(100, 999),
        "projeto":         random.randint(1, 50),
        "centro_custo":    f"M{random.randint(10000, 99999)}",
        "origem":          random.choice(origens),
        "codigo_usuario":  random.randint(100, 999),
        "usuario_lote":    random.choice(usuarios),
        "data_lote":       fake.date_time_this_year()
    }

    dados.append(linha)

df = pd.DataFrame(dados)

df.to_excel("data/lancamentos_contabeis_fake.xlsx", index=False)


print("Dataset gerado com sucesso!")
print(f"Total de lançamentos: {len(df):,}")
print(f"Total Débitos:  R$ {df['debito'].sum():>15,.2f}")
print(f"Total Créditos: R$ {df['credito'].sum():>15,.2f}")
