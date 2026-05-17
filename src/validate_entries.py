import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────
#  CONFIGURAÇÕES
# ─────────────────────────────────────────
ARQUIVO = "data/lancamentos_contabeis_fake.xlsx"
RELATORIO = "reports/relatorio_validacao.txt"

# ─────────────────────────────────────────
#  CARREGAR DADOS
# ─────────────────────────────────────────
print("Carregando lançamentos...")
df = pd.read_excel(ARQUIVO)
total = len(df)
print(f"{total:,} lançamentos carregados.\n")

inconsistencias = {}

# ─────────────────────────────────────────
#  VALIDAÇÃO 1 — Débito E Crédito zerados
# ─────────────────────────────────────────
ambos_zerados = df[(df["debito"] == 0) & (df["credito"] == 0)]
inconsistencias["Débito e crédito zerados"] = ambos_zerados

# ─────────────────────────────────────────
#  VALIDAÇÃO 2 — Débito E Crédito preenchidos
# ─────────────────────────────────────────
ambos_preenchidos = df[(df["debito"] > 0) & (df["credito"] > 0)]
inconsistencias["Débito e crédito simultâneos"] = ambos_preenchidos

# ─────────────────────────────────────────
#  VALIDAÇÃO 3 — Valores negativos
# ─────────────────────────────────────────
negativos = df[(df["debito"] < 0) | (df["credito"] < 0)]
inconsistencias["Valores negativos"] = negativos

# ─────────────────────────────────────────
#  VALIDAÇÃO 4 — Datas futuras
# ─────────────────────────────────────────
df["data_lancamento"] = pd.to_datetime(df["data_lancamento"])
hoje = pd.Timestamp(datetime.today().date())
datas_futuras = df[df["data_lancamento"] > hoje]
inconsistencias["Datas futuras"] = datas_futuras

# ─────────────────────────────────────────
#  VALIDAÇÃO 5 — Conta contábil fora do range
# ─────────────────────────────────────────
conta_invalida = df[(df["conta_contabil"] < 10000) | (df["conta_contabil"] > 99999)]
inconsistencias["Conta contábil inválida"] = conta_invalida

# ─────────────────────────────────────────
#  VALIDAÇÃO 6 — Lançamentos suspeitos
#  (valor acima de R$ 40.000)
# ─────────────────────────────────────────
limite_suspeito = 40000
suspeitos = df[(df["debito"] > limite_suspeito) | (df["credito"] > limite_suspeito)]
inconsistencias["Lançamentos suspeitos (> R$ 40.000)"] = suspeitos

# ─────────────────────────────────────────
#  VALIDAÇÃO 7 — Documentos duplicados
# ─────────────────────────────────────────
duplicados = df[df.duplicated(subset=["documento_seq", "empresa"], keep=False)]
inconsistencias["Documentos duplicados"] = duplicados

# ─────────────────────────────────────────
#  EQUILÍBRIO GERAL — Débitos vs Créditos
# ─────────────────────────────────────────
total_debitos = df["debito"].sum()
total_creditos = df["credito"].sum()
diferenca = round(total_debitos - total_creditos, 2)

# ─────────────────────────────────────────
#  GERAR RELATÓRIO
# ─────────────────────────────────────────
linhas = []
linhas.append("=" * 50)
linhas.append("   RELATÓRIO DE VALIDAÇÃO CONTÁBIL")
linhas.append(f"   Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
linhas.append("=" * 50)
linhas.append(f"\nTotal de lançamentos analisados: {total:,}\n")

linhas.append("-" * 50)
linhas.append("  INCONSISTÊNCIAS ENCONTRADAS")
linhas.append("-" * 50)

encontrou = False
for nome, df_inc in inconsistencias.items():
    qtd = len(df_inc)
    status = "⚠️  ATENÇÃO" if qtd > 0 else "✅ OK"
    linhas.append(f"{status} | {nome}: {qtd:,} registros")
    if qtd > 0:
        encontrou = True

linhas.append("\n" + "-" * 50)
linhas.append("  EQUILÍBRIO DE DÉBITOS E CRÉDITOS")
linhas.append("-" * 50)
linhas.append(f"Total Débitos:  R$ {total_debitos:>15,.2f}")
linhas.append(f"Total Créditos: R$ {total_creditos:>15,.2f}")
linhas.append(f"Diferença:      R$ {diferenca:>15,.2f}")

if diferenca == 0:
    linhas.append("✅ Lançamentos equilibrados.")
else:
    linhas.append("⚠️  ATENÇÃO: Lançamentos NÃO estão equilibrados!")

linhas.append("\n" + "=" * 50)
if encontrou:
    linhas.append("  RESULTADO: VALIDAÇÃO COM PENDÊNCIAS")
else:
    linhas.append("  RESULTADO: VALIDAÇÃO OK — SEM INCONSISTÊNCIAS")
linhas.append("=" * 50)

relatorio = "\n".join(linhas)
print(relatorio)

import os
os.makedirs("reports", exist_ok=True)
with open(RELATORIO, "w", encoding="utf-8") as f:
    f.write(relatorio)

print(f"\nRelatório salvo em: {RELATORIO}")
