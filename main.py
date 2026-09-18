"""
Orquestrador Principal do Pipeline de Dados do PIB Municipal (IBGE - RJ)
Executa o fluxo completo ponta a ponta:
1. Ingestao e Carga no PostgreSQL (ETL)
2. Processamento Estatistico, Visualizacoes e Relatorios (Analytics)
"""

import sys
import time
import subprocess

# Garante saida UTF-8 no console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def log_etapa(numero: int, titulo: str):
    print("\n" + "=" * 80)
    print(f" [ETAPA {numero}] {titulo}")
    print("=" * 80)

def executar_modulo(caminho_script: str, descricao: str):
    inicio = time.time()
    print(f"\n>> Iniciando: {descricao} ({caminho_script})...\n")
    resultado = subprocess.run([sys.executable, caminho_script], check=True)
    duracao = time.time() - inicio
    print(f"\n>> Concluido com sucesso: {descricao} em {duracao:.2f} segundos.")

def main():
    tempo_total_inicio = time.time()
    print("*" * 80)
    print("       PIPELINE DE ENGENHARIA DE DADOS GEOESPACIAIS - PIB IBGE (RJ)")
    print("*" * 80)

    try:
        # Etapa 1: Ingestao ETL (API SIDRA -> PostgreSQL)
        log_etapa(1, "EXTRACAO E CARGA NO POSTGRESQL (ETL)")
        executar_modulo("scripts/etl_pib_ibge.py", "ETL PIB IBGE")

        # Etapa 2: Analise Estatistica e Geracao de Relatorios
        log_etapa(2, "ANALISE EXPLORATORIA, DASHBOARD E RELATORIOS (ANALYTICS)")
        executar_modulo("scripts/analytics.py", "Analytics & Reporting")

        tempo_total = time.time() - tempo_total_inicio
        print("\n" + "=" * 80)
        print(f" [SUCESSO] Pipeline executado com exito em {tempo_total:.2f} segundos!")
        print(" Artefatos disponiveis em:")
        print("   - reports/dashboard_pib_rj.html (Dashboard Interativo)")
        print("   - reports/relatorio_pib_rj.pdf   (Relatorio Executivo)")
        print("   - img/*.png                     (Graficos em Alta Resolucao)")
        print("   - data/                         (Tabelas e Estatisticas Sumarizadas)")
        print("=" * 80 + "\n")

    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO DE EXECUCAO] Falha ao executar subprocesso: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO CRITICO] Ocorreu uma falha no pipeline: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
