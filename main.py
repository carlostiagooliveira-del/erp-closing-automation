import subprocess
import sys
import os
from datetime import datetime

# ─────────────────────────────────────────
#  UTILITÁRIOS
# ─────────────────────────────────────────
def log(msg, tipo="info"):
    hora = datetime.now().strftime("%H:%M:%S")
    icones = {"info": "→", "ok": "✅", "erro": "❌", "titulo": "🏦"}
    print(f"[{hora}] {icones.get(tipo, '→')} {msg}")

def rodar(script, descricao):
    log(f"Iniciando: {descricao}")
    resultado = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if resultado.returncode == 0:
        log(f"Concluído: {descricao}", "ok")
        if resultado.stdout:
            for linha in resultado.stdout.strip().split("\n"):
                print(f"           {linha}")
    else:
        log(f"Erro em: {descricao}", "erro")
        print(resultado.stderr)
        sys.exit(1)

# ─────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────
def menu():
    print("\n" + "=" * 50)
    print("  🏦  ERP CLOSING AUTOMATION")
    print("=" * 50)
    print("  1. Executar pipeline completo")
    print("  2. Gerar dataset")
    print("  3. Validar lançamentos")
    print("  4. Abrir dashboard")
    print("  0. Sair")
    print("=" * 50)
    return input("  Escolha uma opção: ").strip()

# ─────────────────────────────────────────
#  AÇÕES
# ─────────────────────────────────────────
def gerar_dataset():
    rodar("src/generate_dataset.py", "Geração do dataset contábil")

def validar_lancamentos():
    if not os.path.exists("data/lancamentos_contabeis_fake.xlsx"):
        log("Dataset não encontrado. Gere o dataset primeiro.", "erro")
        return
    rodar("src/validate_entries.py", "Validação dos lançamentos")

def abrir_dashboard():
    if not os.path.exists("data/lancamentos_contabeis_fake.xlsx"):
        log("Dataset não encontrado. Gere o dataset primeiro.", "erro")
        return
    log("Abrindo dashboard no navegador...")
    log("Pressione Ctrl+C no terminal para encerrar.", "info")
    subprocess.run(["streamlit", "run", "dashboard/dashboard.py"])

def pipeline_completo():
    log("PIPELINE COMPLETO INICIADO", "titulo")
    print("-" * 50)
    gerar_dataset()
    validar_lancamentos()
    print("-" * 50)
    log("Pipeline finalizado com sucesso!", "ok")
    print()
    abrir = input("  Deseja abrir o dashboard agora? (s/n): ").strip().lower()
    if abrir == "s":
        abrir_dashboard()

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    while True:
        opcao = menu()

        if opcao == "1":
            pipeline_completo()
        elif opcao == "2":
            gerar_dataset()
        elif opcao == "3":
            validar_lancamentos()
        elif opcao == "4":
            abrir_dashboard()
        elif opcao == "0":
            log("Encerrando. Até logo!")
            break
        else:
            log("Opção inválida. Tente novamente.", "erro")