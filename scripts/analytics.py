# =================================================================================================== #
# 1. Configuração Inicial e Carregamento dos Dados
# =================================================================================================== #

# Importação das bibliotecas
import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import linregress
from dotenv import load_dotenv
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from fpdf import FPDF

warnings.filterwarnings('ignore')

# Configuração de encoding para o terminal Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de conexão com o banco de dados PostgreSQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "gisdb")
DB_SCHEMA = os.getenv("DB_SCHEMA", "geoanalytics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
TABLE_NAME = "ibge_pib_municipios_raw"

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '{:,.0f}'.format(x) if abs(x) > 1000 else '{:.2f}'.format(x))

# Função auxiliar para salvamento/sobrescrita dos gráficos no diretório 'img'
def salvar_grafico(filename):
    output_dir = 'img'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    if os.path.exists(output_path):
        os.remove(output_path)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')

# Função auxiliar para cálculo do Coeficiente de Gini
def calcular_gini(array):
    """Calcula o Coeficiente de Gini para um array numérico."""
    array = np.asarray(array, dtype=np.float64)
    if np.amin(array) < 0:
        array -= np.amin(array)
    array = np.sort(array)
    index = np.arange(1, array.shape[0] + 1)
    n = array.shape[0]
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

# Conectar ao banco de dados e carregar os dados via SQL
connection_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_url)

query = f"SELECT * FROM {DB_SCHEMA}.{TABLE_NAME}"
df = pd.read_sql(query, con=engine)

print("\n=== INÍCIO DO CARREGAMENTO DOS DADOS ===")
print(f"Dados carregados do banco de dados ({DB_SCHEMA}.{TABLE_NAME}): {df.shape[0]:,} registros")
print(f"Período: {df['ano'].min()} a {df['ano'].max()}")
print(f"Municípios: {df['id_municipio'].nunique():,}")
print("\n=== FIM DO CARREGAMENTO DOS DADOS ===")

# =================================================================================================== #
# 2. Visão Geral dos Dados
# =================================================================================================== #

print("\n=== INÍCIO DA VISÃO GERAL DOS DADOS ===")

# Estrutura dos dados
print("\n=== ESTRUTURA DOS DADOS ===")
print(df.info())

# Estatísticas descritivas básicas
print("\n=== ESTATÍSTICAS DESCRITIVAS BÁSICAS ===")
print(df['pib_mil_reais'].describe())

# Verificação de dados missing
print(f"\nValores nulos: {df['pib_mil_reais'].isnull().sum():,}")
print(f"Percentual de nulos: {df['pib_mil_reais'].isnull().mean()*100:.2f}%")

# Distribuição por UF (foco no RJ)
print("\n=== DISTRIBUIÇÃO POR UF ===")
print(df['uf'].value_counts())

print("\n=== FIM DA VISÃO GERAL DOS DADOS ===")

# =================================================================================================== #
# 3. Análise Temporal Agregada
# =================================================================================================== #

print("\n=== INÍCIO DA ANÁLISE TEMPORAL AGREGADA ===")

# PIB total por ano (soma de todos os municípios)
pib_anual = df.groupby('ano')['pib_mil_reais'].sum().reset_index()
pib_anual['pib_milhoes'] = pib_anual['pib_mil_reais'] / 1000
pib_anual['pib_bilhoes'] = pib_anual['pib_mil_reais'] / 1000000

print("\n=== PIB TOTAL DO RJ POR ANO (EM BILHÕES R$) ===")
for _, row in pib_anual.iterrows():
    print(f"{row['ano']}: R$ {row['pib_bilhoes']:.2f} bilhões")

# Variação percentual anual
pib_anual['variacao_pct'] = pib_anual['pib_bilhoes'].pct_change() * 100
print("\n=== VARIAÇÃO PERCENTUAL ANUAL ===")
for i in range(1, len(pib_anual)):
    ano = pib_anual.iloc[i]['ano']
    variacao = pib_anual.iloc[i]['variacao_pct']
    print(f"{ano}: {variacao:+.2f}%")

# Gráfico da evolução do PIB total
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(pib_anual['ano'], pib_anual['pib_bilhoes'], marker='o', linewidth=2)
ax1.set_title('Evolução do PIB Total do RJ (2015-2023)', fontsize=14)
ax1.set_xlabel('Ano')
ax1.set_ylabel('PIB (bilhões R$)')
ax1.grid(True, alpha=0.3)
for x, y in zip(pib_anual['ano'], pib_anual['pib_bilhoes']):
    ax1.annotate(f'R$ {y:.1f}B', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

ax2.bar(pib_anual['ano'], pib_anual['variacao_pct'])
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax2.set_title('Variação Percentual Anual do PIB', fontsize=14)
ax2.set_xlabel('Ano')
ax2.set_ylabel('Variação (%)')
ax2.grid(True, alpha=0.3)

salvar_grafico('pib_evolucao_total.png')
plt.show()

print("\n=== FIM DA ANÁLISE TEMPORAL AGREGADA ===")

# =================================================================================================== #
# 4. Análise Estatística Descritiva por Município
# =================================================================================================== #

print("\n=== INÍCIO DA ANÁLISE ESTATÍSTICA DESCRITIVA POR MUNICÍPIO ===")

# Estatísticas por município (média, mediana, mínimo, máximo, desvio padrão)
stats_municipios = df.groupby(['id_municipio', 'nome_municipio']).agg({
    'pib_mil_reais': [
        'mean',      # média
        'median',    # mediana
        'min',       # mínimo
        'max',       # máximo
        'std',       # desvio padrão
        'count'      # contagem (anos disponíveis)
    ]
}).round(2)

# Renomeando colunas
stats_municipios.columns = ['media', 'mediana', 'minimo', 'maximo', 'desvio_padrao', 'anos']
stats_municipios = stats_municipios.reset_index()

# Adicionando colunas derivadas
stats_municipios['amplitude'] = stats_municipios['maximo'] - stats_municipios['minimo']
stats_municipios['cv'] = (stats_municipios['desvio_padrao'] / stats_municipios['media']) * 100  # Coeficiente de Variação (%)
stats_municipios['variacao_total'] = ((stats_municipios['maximo'] - stats_municipios['minimo']) / stats_municipios['minimo']) * 100

print("\n=== TOP 10 MUNICÍPIOS POR PIB MÉDIO (EM MIL R$) ===")
print(stats_municipios.nlargest(10, 'media')[['nome_municipio', 'media', 'mediana', 'maximo']])

print("\n=== TOP 10 MUNICÍPIOS POR MAIOR CRESCIMENTO (2015-2023) ===")
# Pegando valores específicos de 2015 e 2023
pib_2015 = df[df['ano'] == 2015][['id_municipio', 'pib_mil_reais']].rename(columns={'pib_mil_reais': 'pib_2015'})
pib_2023 = df[df['ano'] == 2023][['id_municipio', 'pib_mil_reais']].rename(columns={'pib_mil_reais': 'pib_2023'})
crescimento = pd.merge(pib_2015, pib_2023, on='id_municipio')
crescimento['crescimento_pct'] = ((crescimento['pib_2023'] - crescimento['pib_2015']) / crescimento['pib_2015']) * 100
crescimento = crescimento.merge(df[['id_municipio', 'nome_municipio']].drop_duplicates(), on='id_municipio')
crescimento_top10 = crescimento.nlargest(10, 'crescimento_pct')
for _, row in crescimento_top10.iterrows():
    print(f"{row['nome_municipio']}: {row['crescimento_pct']:.1f}%")

print("\n=== FIM DA ANÁLISE ESTATÍSTICA DESCRITIVA POR MUNICÍPIO ===")

# =================================================================================================== #
# 5. Análise de Distribuição e Outliers
# =================================================================================================== #

print("\n=== INÍCIO DA ANÁLISE DE DISTRIBUIÇÃO E OUTLIERS ===")

# Análise de distribuição dos valores de PIB
print("\n=== ANÁLISE DE DISTRIBUIÇÃO DO PIB ===")

# Medidas de assimetria e curtose
assimetria = df['pib_mil_reais'].skew()
curtose = df['pib_mil_reais'].kurtosis()
print(f"Assimetria (Skewness): {assimetria:.2f} (Positiva = cauda à direita)")
print(f"Curtose (Kurtosis): {curtose:.2f} (Leptocúrtica = caudas pesadas)")

# Quantis
quantis = df['pib_mil_reais'].quantile([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
print("\n=== QUANTIS DO PIB (EM MIL R$) ===")
for q, v in quantis.items():
    print(f"Q{int(q*100):02d}: R$ {v:,.0f}")

# Detecção de outliers usando IQR
Q1 = df['pib_mil_reais'].quantile(0.25)
Q3 = df['pib_mil_reais'].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

outliers = df[(df['pib_mil_reais'] < limite_inferior) | (df['pib_mil_reais'] > limite_superior)]
print(f"\nOutliers identificados: {len(outliers):,} registros ({len(outliers)/len(df)*100:.2f}% do total)")
print(f"Limite inferior: R$ {limite_inferior:,.0f}")
print(f"Limite superior: R$ {limite_superior:,.0f}")

# Visualização da distribuição
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Histograma com KDE (escala log por causa da assimetria)
df_log = df.copy()
df_log['log_pib'] = np.log10(df['pib_mil_reais'] + 1)  # +1 para evitar log(0)
ax1.hist(df_log['log_pib'], bins=50, alpha=0.7, edgecolor='black')
ax1.set_title('Distribuição do PIB (Escala Log)', fontsize=14)
ax1.set_xlabel('Log10(PIB em Mil R$)')
ax1.set_ylabel('Frequência')
ax1.axvline(x=np.mean(df_log['log_pib']), color='red', linestyle='--', label=f'Média: {np.mean(df_log["log_pib"]):.2f}')
ax1.axvline(x=np.median(df_log['log_pib']), color='green', linestyle='--', label=f'Mediana: {np.median(df_log["log_pib"]):.2f}')
ax1.legend()

# Boxplot por ano
sns.boxplot(data=df, x='ano', y=np.log10(df['pib_mil_reais'] + 1), ax=ax2)
ax2.set_title('Distribuição do PIB por Ano (Escala Log)', fontsize=14)
ax2.set_xlabel('Ano')
ax2.set_ylabel('Log10(PIB em Mil R$)')
ax2.tick_params(axis='x', rotation=45)

salvar_grafico('pib_distribuicao.png')
plt.show()

print("\n=== FIM DA ANÁLISE DE DISTRIBUIÇÃO E OUTLIERS ===")

# =================================================================================================== #
# 6. Análise de Concentração e Desigualdade
# =================================================================================================== #

print("\n=== INÍCIO DA ANÁLISE DE CONCENTRAÇÃO E DESIGUALDADE ===")

# PIB total por município (média)
pib_municipio = df.groupby('nome_municipio')['pib_mil_reais'].mean().sort_values(ascending=False)
gini_coef = calcular_gini(pib_municipio.values)
print(f"\n=== CONCENTRAÇÃO DO PIB ===")
print(f"Índice de Gini: {gini_coef:.3f} (0=igualdade perfeita, 1=desigualdade máxima)")

# Percentual acumulado por município
pib_cumsum = pib_municipio.cumsum()
pib_cumsum_pct = (pib_cumsum / pib_municipio.sum()) * 100

print("\n=== CONCENTRAÇÃO DO PIB NOS MUNICÍPIOS ===")
for pct in [10, 20, 30, 50]:
    n_municipios = (pib_cumsum_pct <= pct).sum()
    print(f"Os {n_municipios} maiores municípios ({(n_municipios/len(pib_municipio))*100:.1f}%) representam {pct}% do PIB")

# Top 5 municípios por PIB médio
top5 = pib_municipio.head(5)
print(f"\nOs 5 maiores municípios representam {(top5.sum()/pib_municipio.sum())*100:.1f}% do PIB total")
for nome, valor in top5.items():
    pct = (valor / pib_municipio.sum()) * 100
    print(f"  {nome}: R$ {valor:,.0f} mil ({pct:.1f}%)")

# Visualização da Curva de Lorenz
fig, ax = plt.subplots(figsize=(8, 8))

# Curva de Lorenz
pib_sorted = np.sort(pib_municipio.values)
pib_cum = np.cumsum(pib_sorted) / np.sum(pib_sorted)
pib_cum = np.insert(pib_cum, 0, 0)
x = np.linspace(0, 1, len(pib_cum))

ax.plot(x, x, 'k--', label='Igualdade Perfeita', linewidth=1)
ax.plot(x, pib_cum, 'b-', label=f'Curva de Lorenz (Gini={gini_coef:.3f})', linewidth=2)
ax.fill_between(x, x, pib_cum, alpha=0.2)
ax.set_title('Curva de Lorenz - Concentração do PIB nos Municípios do RJ', fontsize=14)
ax.set_xlabel('Proporção acumulada de municípios')
ax.set_ylabel('Proporção acumulada do PIB')
ax.legend()
ax.grid(True, alpha=0.3)

salvar_grafico('pib_curva_lorenz.png')
plt.show()

print("\n=== FIM DA ANÁLISE DE CONCENTRAÇÃO E DESIGUALDADE ===")

# =================================================================================================== #
# 7. Análise de Correlação Temporal
# =================================================================================================== #

print("\n=== INÍCIO DA ANÁLISE DE CORRELAÇÃO TEMPORAL ===")

# Matriz de correlação entre anos (como os municípios se comportam ao longo do tempo)
pib_pivot = df.pivot(index='id_municipio', columns='ano', values='pib_mil_reais')
correlacao_anos = pib_pivot.corr()

print("\n=== CORRELAÇÃO ENTRE ANOS ===")
print("Matriz de correlação (apenas alguns valores):")
print(correlacao_anos.round(2))

# Visualização da correlação
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlacao_anos, annot=True, cmap='coolwarm', center=0,
            fmt='.2f', square=True, linewidths=0.5)
ax.set_title('Matriz de Correlação do PIB entre Anos', fontsize=14)
salvar_grafico('pib_correlacao_anos.png')
plt.show()

# Tendência de crescimento por município (regressão linear simples)
def calcular_tendencia(grupo):
    if len(grupo) >= 3:
        slope, intercept, r_value, p_value, std_err = linregress(grupo['ano'], grupo['pib_mil_reais'])
        return pd.Series({
            'tendencia': slope,
            'r2': r_value**2,
            'p_value': p_value
        })
    return pd.Series({'tendencia': np.nan, 'r2': np.nan, 'p_value': np.nan})

tendencias = df.groupby('id_municipio').apply(calcular_tendencia, include_groups=False).reset_index()
tendencias = tendencias.merge(df[['id_municipio', 'nome_municipio']].drop_duplicates(), on='id_municipio')

# Municípios com maior crescimento anual
print("\n=== TOP 10 MUNICÍPIOS COM MAIOR TENDÊNCIA DE CRESCIMENTO (R$ MIL/ANO) ===")
crescimento_anual = tendencias.nlargest(10, 'tendencia')
for _, row in crescimento_anual.iterrows():
    print(f"{row['nome_municipio']}: +R$ {row['tendencia']:,.0f} mil/ano (R²={row['r2']:.2f})")
print("\n=== FIM DA ANÁLISE DE CORRELAÇÃO TEMPORAL ===")

# =================================================================================================== #
# 8. Análise de Sazonalidade e Padrões Temporais
# =================================================================================================== #

print("\n=== INÍCIO DA ANÁLISE DE SAZONALIDADE E PADRÕES TEMPORAIS ===")

# Evolução temporal dos principais municípios
top5_municipios = df.groupby('nome_municipio')['pib_mil_reais'].mean().nlargest(5).index

fig, ax = plt.subplots(figsize=(14, 7))

for municipio in top5_municipios:
    dados = df[df['nome_municipio'] == municipio]
    ax.plot(dados['ano'], dados['pib_mil_reais'] / 1e6,
            marker='o', linewidth=2, label=municipio)

ax.set_title('Evolução do PIB dos 5 Maiores Municípios do RJ (em bilhões R$)', fontsize=14)
ax.set_xlabel('Ano')
ax.set_ylabel('PIB (bilhões R$)')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)

salvar_grafico('pib_top5_municipios.png')
plt.show()

# Taxa de crescimento médio por município (CAGR)
def calcular_cagr(grupo):
    if len(grupo) >= 2:
        pib_inicial = grupo[grupo['ano'] == grupo['ano'].min()]['pib_mil_reais'].iloc[0]
        pib_final = grupo[grupo['ano'] == grupo['ano'].max()]['pib_mil_reais'].iloc[0]
        anos = grupo['ano'].max() - grupo['ano'].min()
        if pib_inicial > 0:
            cagr = (pib_final / pib_inicial) ** (1/anos) - 1
            return cagr * 100
    return np.nan

cagr_municipios = df.groupby('nome_municipio').apply(calcular_cagr).dropna()
cagr_municipios = cagr_municipios.sort_values(ascending=False)

print("\n=== TAXA DE CRESCIMENTO ANUAL (CAGR) - TOP 10 ===")
for municipio, cagr in cagr_municipios.head(10).items():
    print(f"{municipio}: {cagr:.1f}% ao ano")

print("\n=== TAXA DE CRESCIMENTO ANUAL (CAGR) - BOTTOM 10 ===")
for municipio, cagr in cagr_municipios.tail(10).items():
    print(f"{municipio}: {cagr:.1f}% ao ano")

# Distribuição do CAGR
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.hist(cagr_municipios, bins=20, alpha=0.7, edgecolor='black')
ax1.axvline(x=0, color='red', linestyle='--', linewidth=2)
ax1.set_title('Distribuição das Taxas de Crescimento (CAGR)', fontsize=14)
ax1.set_xlabel('CAGR (%)')
ax1.set_ylabel('Número de Municípios')

ax2.boxplot(cagr_municipios)
ax2.set_title('Boxplot do CAGR', fontsize=14)
ax2.set_ylabel('CAGR (%)')
ax2.axhline(y=0, color='red', linestyle='--', linewidth=1)

salvar_grafico('pib_cagr_distribuicao.png')
plt.show()

print("\n=== FIM DA ANÁLISE DE SAZONALIDADE E PADRÕES TEMPORAIS ===")

# =================================================================================================== #
# 9. Análise de Performance Relativa
# =================================================================================================== #

print("\n=== INÍCIO DA ANÁLISE DE PERFORMANCE RELATIVA ===")

# Performance relativa - comparando com a média do estado
media_anual = df.groupby('ano')['pib_mil_reais'].mean().reset_index()
media_anual.columns = ['ano', 'media_estadual']

df_comparacao = df.merge(media_anual, on='ano')
df_comparacao['performance'] = (df_comparacao['pib_mil_reais'] / df_comparacao['media_estadual']) * 100

# Municípios com melhor performance relativa
performance_municipios = df_comparacao.groupby('nome_municipio')['performance'].mean().sort_values(ascending=False)
print("\n=== MUNICÍPIOS COM MELHOR PERFORMANCE RELATIVA (média) ===")
for municipio, perf in performance_municipios.head(10).items():
    print(f"{municipio}: {perf:.1f}% da média estadual")

# Matriz de posição relativa
fig, ax = plt.subplots(figsize=(14, 6))

# Heatmap da performance relativa
performance_pivot = df_comparacao.pivot_table(
    index='nome_municipio',
    columns='ano',
    values='performance'
).fillna(0)

# Selecionar apenas os 30 maiores municípios para visualização
top30 = performance_municipios.head(30).index
performance_top30 = performance_pivot.loc[top30]

sns.heatmap(performance_top30, cmap='RdBu_r', center=100,
            annot=False, linewidths=0.1, cbar_kws={'label': 'Performance (% da média)'})
ax.set_title('Performance Relativa dos 30 Maiores Municípios (%)', fontsize=14)
ax.set_xlabel('Ano')
ax.set_ylabel('Município')

salvar_grafico('pib_heatmap_performance.png')
plt.show()
print("\n=== FIM DA ANÁLISE DE PERFORMANCE RELATIVA ===")

# =================================================================================================== #
# 10. Relatório Resumo e Salvamento dos Dados
# =================================================================================================== #

print("\n=== INÍCIO DO RELATÓRIO RESUMITIVO ===")

print("\n" + "="*60)
print("RELATÓRIO RESUMO - ANÁLISE EXPLORATÓRIA DO PIB DOS MUNICÍPIOS DO RJ")
print("="*60)

print(f"\n1. PERÍODO ANALISADO: {df['ano'].min()} a {df['ano'].max()}")
print(f"   - Total de registros: {len(df):,}")
print(f"   - Número de municípios: {df['id_municipio'].nunique():,}")

print(f"\n2. ESTATÍSTICAS GERAIS DO PIB (em mil R$):")
print(f"   - Média: R$ {df['pib_mil_reais'].mean():,.0f}")
print(f"   - Mediana: R$ {df['pib_mil_reais'].median():,.0f}")
print(f"   - Desvio Padrão: R$ {df['pib_mil_reais'].std():,.0f}")
print(f"   - Coeficiente de Variação: {(df['pib_mil_reais'].std()/df['pib_mil_reais'].mean())*100:.1f}%")
print(f"   - Mínimo: R$ {df['pib_mil_reais'].min():,.0f}")
print(f"   - Máximo: R$ {df['pib_mil_reais'].max():,.0f}")

print(f"\n3. EVOLUÇÃO TEMPORAL:")
for ano in [2015, 2018, 2021, 2023]:
    pib_ano = df[df['ano'] == ano]['pib_mil_reais'].sum()
    pib_ano_bilhoes = pib_ano / 1_000_000
    print(f"   - {ano}: R$ {pib_ano_bilhoes:.2f} bilhões")

crescimento_total = ((df[df['ano']==2023]['pib_mil_reais'].sum() / df[df['ano']==2015]['pib_mil_reais'].sum()) - 1) * 100
print(f"   - Crescimento total (2015-2023): {crescimento_total:.1f}%")

print(f"\n4. CONCENTRAÇÃO:")
print(f"   - Índice de Gini: {gini_coef:.3f}")
pct_top5 = (top5.sum() / pib_municipio.sum()) * 100
print(f"   - Top 5 municípios representam {pct_top5:.1f}% do PIB")

print(f"\n5. DISTRIBUIÇÃO:")
print(f"   - Assimetria: {assimetria:.2f}")
print(f"   - Curtose: {curtose:.2f}")
print(f"   - % de outliers: {(len(outliers)/len(df))*100:.2f}%")

print(f"\n6. CRESCIMENTO (CAGR médio): {cagr_municipios.mean():.1f}%")
print(f"   - Melhor CAGR: {cagr_municipios.max():.1f}%")
print(f"   - Pior CAGR: {cagr_municipios.min():.1f}%")
print(f"   - Mediana do CAGR: {cagr_municipios.median():.1f}%")

# Salvar estatísticas em CSV no diretório 'data'
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)
csv_output_path = os.path.join(data_dir, 'estatisticas_pib_municipios.csv')

stats_municipios.to_csv(csv_output_path, index=False)
print(f"\n✓ Estatísticas detalhadas salvas em '{csv_output_path}'")
print("\n=== FIM DO RELATÓRIO RESUMITIVO ===")


# =================================================================================================== #
# 11. Geração do Dashboard HTML Interativo (Plotly + todos os resultados da EDA)
# =================================================================================================== #

def gerar_dashboard_html():
    print("\n=== GERAÇÃO DO DASHBOARD HTML INTERATIVO ===")
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)
    html_filepath = os.path.join(reports_dir, 'dashboard_pib_rj.html')

    # ---- Gráficos Plotly interativos ----

    # Fig 1: Evolução temporal + variação anual
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Bar(x=pib_anual['ano'], y=pib_anual['variacao_pct'],
                          name="Variação Anual (%)", marker_color='#00A4EF', opacity=0.85),
                   secondary_y=True)
    fig1.add_trace(go.Scatter(x=pib_anual['ano'], y=pib_anual['pib_bilhoes'],
                              name="PIB Total (R$ Bi)", mode='lines+markers+text',
                              text=[f"R$ {v:.1f}B" for v in pib_anual['pib_bilhoes']],
                              textposition="top center",
                              line=dict(color='#01579B', width=4), marker=dict(size=10)),
                   secondary_y=False)
    fig1.update_layout(title="<b>Evolução do PIB Total do Estado do Rio de Janeiro (2015-2023)</b>",
                       paper_bgcolor='white', plot_bgcolor='#F8F9FA', height=450,
                       font=dict(family="'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif", color='#323232'),
                       margin=dict(l=40, r=40, t=60, b=40),
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig1.update_xaxes(title_text="Ano", gridcolor='#D0D1D3', dtick=1)
    fig1.update_yaxes(title_text="PIB Total (Bilhões R$)", secondary_y=False, gridcolor='#D0D1D3')
    fig1.update_yaxes(title_text="Variação Anual (%)", secondary_y=True)

    # Fig 2: Top 10 por PIB Médio
    top10_df = stats_municipios.nlargest(10, 'media').sort_values('media', ascending=True)
    fig2 = go.Figure(go.Bar(
        x=top10_df['media'] / 1e6, y=top10_df['nome_municipio'], orientation='h',
        marker=dict(color=top10_df['media'], colorscale='Blues'),
        text=[f"R$ {v/1e6:.2f} Bi" for v in top10_df['media']], textposition='outside'
    ))
    fig2.update_layout(title="<b>Top 10 Municípios por PIB Médio (2015-2023)</b>",
                       paper_bgcolor='white', plot_bgcolor='#F8F9FA', height=440,
                       font=dict(family="'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif", color='#323232'),
                       margin=dict(l=40, r=80, t=60, b=40))
    fig2.update_xaxes(title_text="PIB Médio (Bilhões R$)", gridcolor='#D0D1D3')

    # Fig 3: Evolução Top 5 Municípios
    fig3 = go.Figure()
    colors = ['#01579B', '#00A4EF', '#0079C1', '#35AC46', '#E8A904']
    for idx, mun in enumerate(top5_municipios):
        mun_data = df[df['nome_municipio'] == mun].sort_values('ano')
        fig3.add_trace(go.Scatter(x=mun_data['ano'], y=mun_data['pib_mil_reais'] / 1e6,
                                  name=mun, mode='lines+markers',
                                  line=dict(width=3, color=colors[idx % len(colors)]),
                                  marker=dict(size=8)))
    fig3.update_layout(title="<b>Evolução do PIB dos 5 Maiores Municípios (Bilhões R$)</b>",
                       paper_bgcolor='white', plot_bgcolor='#F8F9FA', height=440,
                       font=dict(family="'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif", color='#323232'),
                       margin=dict(l=40, r=40, t=60, b=40),
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig3.update_xaxes(title_text="Ano", gridcolor='#D0D1D3', dtick=1)
    fig3.update_yaxes(title_text="PIB (Bilhões R$)", gridcolor='#D0D1D3')

    # Fig 4: Curva de Lorenz
    pib_sorted_l = np.sort(pib_municipio.values)
    pib_cum_l = np.cumsum(pib_sorted_l) / np.sum(pib_sorted_l)
    pib_cum_l = np.insert(pib_cum_l, 0, 0)
    x_lorenz = np.linspace(0, 1, len(pib_cum_l))
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=x_lorenz, y=x_lorenz, name='Igualdade Perfeita',
                              line=dict(color='#BBBCBE', dash='dash')))
    fig4.add_trace(go.Scatter(x=x_lorenz, y=pib_cum_l,
                              name=f'Curva de Lorenz (Gini={gini_coef:.3f})',
                              fill='tonexty', fillcolor='rgba(1,87,155,0.15)',
                              line=dict(color='#01579B', width=3)))
    fig4.update_layout(title=f"<b>Concentração do PIB — Curva de Lorenz (Gini: {gini_coef:.3f})</b>",
                       paper_bgcolor='white', plot_bgcolor='#F8F9FA', height=440,
                       font=dict(family="'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif", color='#323232'),
                       margin=dict(l=40, r=40, t=60, b=40),
                       legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    fig4.update_xaxes(title_text="Proporção Acumulada de Municípios", gridcolor='#D0D1D3')
    fig4.update_yaxes(title_text="Proporção Acumulada do PIB", gridcolor='#D0D1D3')

    # Fig 5: CAGR — Top 10 e Bottom 10
    top10_cagr = cagr_municipios.head(10).reset_index()
    top10_cagr.columns = ['municipio', 'cagr']
    bottom10_cagr = cagr_municipios.tail(10).reset_index()
    bottom10_cagr.columns = ['municipio', 'cagr']
    cagr_combined = pd.concat([top10_cagr, bottom10_cagr]).sort_values('cagr', ascending=True)
    fig5 = go.Figure(go.Bar(
        x=cagr_combined['cagr'], y=cagr_combined['municipio'], orientation='h',
        marker=dict(color=['#D32F2F' if v < 0 else '#01579B' for v in cagr_combined['cagr']]),
        text=[f"{v:+.1f}%" for v in cagr_combined['cagr']], textposition='outside'
    ))
    fig5.update_layout(title="<b>CAGR 2015–2023 — Maiores e Menores Crescimentos</b>",
                       paper_bgcolor='white', plot_bgcolor='#F8F9FA', height=480,
                       font=dict(family="'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif", color='#323232'),
                       margin=dict(l=40, r=80, t=60, b=40))
    fig5.update_xaxes(title_text="CAGR Anual (%)", gridcolor='#D0D1D3')

    # Fig 6: Distribuição do PIB (Histograma log + Boxplot por ano)
    log_pib_mean = df_log['log_pib'].mean()
    log_pib_median = df_log['log_pib'].median()
    fig6 = make_subplots(rows=1, cols=2, subplot_titles=("Distribuição do PIB (Log10)", "Distribuição por Ano"))
    fig6.add_trace(go.Histogram(x=df_log['log_pib'], marker_color='#00A4EF', opacity=0.85, name='Frequência'), row=1, col=1)
    fig6.add_vline(x=log_pib_mean, line_dash='dash', line_color='#D32F2F',
                   annotation_text=f"Média: {log_pib_mean:.2f}", annotation_position="top", row=1, col=1)
    fig6.add_vline(x=log_pib_median, line_dash='dash', line_color='#35AC46',
                   annotation_text=f"Mediana: {log_pib_median:.2f}", annotation_position="bottom", row=1, col=1)
    fig6.add_trace(go.Box(x=df['ano'], y=df_log['log_pib'], marker_color='#01579B',
                          name='PIB por Ano', showlegend=False), row=1, col=2)
    fig6.update_layout(title="<b>Distribuição do PIB e Detecção de Outliers</b>",
                       paper_bgcolor='white', plot_bgcolor='#F8F9FA', height=420,
                       font=dict(family="'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif", color='#323232'),
                       margin=dict(l=40, r=40, t=80, b=40), showlegend=False)
    fig6.update_xaxes(title_text="Log10(PIB em Mil R$)", gridcolor='#D0D1D3', row=1, col=1)
    fig6.update_yaxes(title_text="Frequência", gridcolor='#D0D1D3', row=1, col=1)
    fig6.update_xaxes(title_text="Ano", gridcolor='#D0D1D3', row=1, col=2)
    fig6.update_yaxes(title_text="Log10(PIB em Mil R$)", gridcolor='#D0D1D3', row=1, col=2)

    # Fig 7: Distribuição das Taxas de Crescimento (CAGR)
    cagr_neg = cagr_municipios[cagr_municipios < 0]
    cagr_pos = cagr_municipios[cagr_municipios >= 0]
    fig7 = make_subplots(rows=1, cols=2, subplot_titles=("Distribuição do CAGR", "Boxplot do CAGR"))
    fig7.add_trace(go.Histogram(x=cagr_neg, marker_color='#D32F2F', opacity=0.85, name='CAGR < 0'), row=1, col=1)
    fig7.add_trace(go.Histogram(x=cagr_pos, marker_color='#01579B', opacity=0.85, name='CAGR ≥ 0'), row=1, col=1)
    fig7.add_vline(x=0, line_dash='dash', line_color='#545454', row=1, col=1)
    fig7.add_trace(go.Box(y=cagr_municipios, marker_color='#01579B', name='CAGR', showlegend=False), row=1, col=2)
    fig7.add_hline(y=0, line_dash='dash', line_color='#545454', row=1, col=2)
    fig7.update_layout(title="<b>Distribuição das Taxas de Crescimento (CAGR)</b>",
                       paper_bgcolor='white', plot_bgcolor='#F8F9FA', height=420,
                       font=dict(family="'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif", color='#323232'),
                       margin=dict(l=40, r=40, t=80, b=40), barmode='overlay',
                       legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1))
    fig7.update_xaxes(title_text="CAGR (%)", gridcolor='#D0D1D3', row=1, col=1)
    fig7.update_yaxes(title_text="Número de Municípios", gridcolor='#D0D1D3', row=1, col=1)
    fig7.update_yaxes(title_text="CAGR (%)", gridcolor='#D0D1D3', row=1, col=2)

    # ---- Dados calculados para KPIs ----
    pib_2023_val = pib_anual.iloc[-1]['pib_bilhoes']

    # Correlações entre pares distintos de anos (triângulo superior da matriz)
    corr_vals = correlacao_anos.values[np.triu_indices_from(correlacao_anos.values, 1)]

    # Concentração no topo do ranking (para os textos analíticos)
    pct_top10 = (pib_municipio.nlargest(10).sum() / pib_municipio.sum()) * 100
    pct_rio = (pib_municipio.loc['Rio de Janeiro'] / pib_municipio.sum()) * 100

    # ---- Montar tabelas HTML ----

    # Tabela mestra: consolida estatísticas descritivas, CAGR e tendência linear por município
    def tabela_mestra_municipios_html():
        df_t = (stats_municipios
                .merge(tendencias[['nome_municipio', 'tendencia', 'r2']], on='nome_municipio', how='left')
                .assign(cagr=lambda d: d['nome_municipio'].map(cagr_municipios))
                .sort_values('media', ascending=False))
        rows = ""
        for _, r in df_t.iterrows():
            cor_cagr = "#35AC46" if r['cagr'] >= 0 else "#D32F2F"
            rows += f"""
            <tr>
                <td><b>{r['nome_municipio']}</b></td>
                <td>R$ {r['media']:,.0f}</td>
                <td>R$ {r['mediana']:,.0f}</td>
                <td>R$ {r['minimo']:,.0f}</td>
                <td>R$ {r['maximo']:,.0f}</td>
                <td>R$ {r['desvio_padrao']:,.0f}</td>
                <td>{r['cv']:.1f}%</td>
                <td style="color:{cor_cagr};font-weight:600">{r['cagr']:.1f}%</td>
                <td>R$ {r['tendencia']:,.0f}</td>
                <td>{r['r2']:.2f}</td>
            </tr>"""
        return f"""
        <table>
            <thead><tr>
                <th>Município</th><th>PIB Médio (Mil R$)</th><th>Mediana</th>
                <th>Mínimo</th><th>Máximo</th><th>Desvio Padrão</th>
                <th>CV (%)</th><th>CAGR (%/ano)</th>
                <th>Tendência (R$ Mil/ano)</th><th>R²</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>"""

    # Tabela de quantis (apêndice metodológico)
    def tabela_quantis_html():
        rows = ""
        for q, v in quantis.items():
            rows += f"<tr><td>Q{int(q*100):02d}</td><td>R$ {v:,.0f}</td></tr>"
        return f"""
        <table>
            <thead><tr><th>Percentil</th><th>PIB (Mil R$)</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>"""

    # ---- Montar HTML final ----
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel do PIB Municipal — Governo do Estado do Rio de Janeiro</title>
    <style>
        :root {{
            --color-primary: #01579B;
            --color-primary-hover: #004A7A;
            --color-primary-light: #00A4EF;
            --color-info: #0079C1;
            --color-success: #35AC46;
            --color-warning: #E8A904;
            --color-error: #D32F2F;
            --color-bg: #FFFFFF;
            --color-bg-secondary: #F8F9FA;
            --color-bg-hover: #EAF3FA;
            --color-border: #D0D1D3;
            --color-text: #323232;
            --color-text-secondary: #545454;
            --font-family: 'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
            --radius-sm: 2px;
            --radius-md: 4px;
            --radius-lg: 8px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
            --shadow-md: 0 3px 6px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.12);
        }}
        *, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; font-family: var(--font-family); }}
        body {{ background-color: var(--color-bg-secondary); color: var(--color-text); padding: 24px; }}
        header {{
            background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
            color: white; padding: 32px 40px; border-radius: var(--radius-lg);
            margin-bottom: 24px; box-shadow: var(--shadow-md);
        }}
        header h1 {{ font-size: 32px; font-weight: 700; letter-spacing: -0.5px; margin-bottom: 6px; }}
        header p {{ font-size: 14px; color: rgba(255,255,255,0.8); }}
        .section-title {{
            font-size: 18px; font-weight: 600; color: var(--color-text);
            padding: 12px 0 8px 0; border-bottom: 2px solid var(--color-border); margin-bottom: 16px;
        }}
        .section-badge {{
            display: inline-block; background: var(--color-primary); color: white;
            font-size: 11px; font-weight: 700; border-radius: var(--radius-sm);
            padding: 3px 10px; margin-right: 8px; vertical-align: middle;
        }}
        .kpi-grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px; margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--color-bg); padding: 20px; border-radius: var(--radius-md);
            border: 1px solid var(--color-border); box-shadow: var(--shadow-sm);
        }}
        .kpi-title {{ font-size: 12px; color: var(--color-text-secondary); font-weight: 600; text-transform: uppercase; margin-bottom: 8px; }}
        .kpi-value {{ font-size: 26px; font-weight: 700; color: var(--color-text); }}
        .kpi-sub {{ font-size: 12px; font-weight: 600; margin-top: 4px; color: var(--color-success); }}
        .kpi-sub.warn {{ color: var(--color-error); }}
        .card {{
            background: var(--color-bg); padding: 24px; border-radius: var(--radius-md);
            border: 1px solid var(--color-border); box-shadow: var(--shadow-sm);
            margin-bottom: 24px; transition: box-shadow 200ms ease-out;
        }}
        .card:hover {{ box-shadow: var(--shadow-md); }}
        .summary-card {{
            background: var(--color-bg); padding: 28px 32px; border-radius: var(--radius-md);
            border: 1px solid var(--color-border); border-left: 4px solid var(--color-primary);
            box-shadow: var(--shadow-sm); margin-bottom: 24px;
        }}
        .summary-card h3 {{ font-size: 20px; font-weight: 700; color: var(--color-text); margin-bottom: 14px; }}
        .summary-card p {{ font-size: 14px; color: var(--color-text); line-height: 1.7; margin-bottom: 12px; }}
        .summary-card p:last-child {{ margin-bottom: 0; }}
        .analise {{ margin-top: 16px; }}
        .analise summary {{
            cursor: pointer; font-size: 13px; font-weight: 600; color: var(--color-primary);
            list-style: none; outline: none; user-select: none;
        }}
        .analise summary::-webkit-details-marker {{ display: none; }}
        .analise summary::before {{ content: '▸ '; }}
        .analise[open] summary::before {{ content: '▾ '; }}
        .analise summary:focus-visible {{ outline: 2px solid var(--color-primary); outline-offset: 2px; }}
        .analise p {{
            font-size: 13px; color: var(--color-text-secondary); line-height: 1.6; margin-top: 10px;
            padding: 12px 14px; background: var(--color-bg-secondary); border-radius: var(--radius-md);
            border-left: 3px solid var(--color-primary);
        }}
        .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }}
        .stat-box {{
            background: var(--color-bg-secondary); border-radius: var(--radius-md); padding: 14px;
            border: 1px solid var(--color-border); margin-bottom: 12px;
        }}
        .stat-box h4 {{ font-size: 13px; color: var(--color-text-secondary); margin-bottom: 6px; }}
        .stat-box p {{ font-size: 14px; color: var(--color-text); font-weight: 600; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 13px; }}
        th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--color-border); }}
        th {{ background-color: var(--color-bg-secondary); font-weight: 700; color: var(--color-text-secondary); font-size: 12px; }}
        tr {{ transition: background-color 200ms ease-out; }}
        tr:hover {{ background-color: var(--color-bg-hover); }}
        .img-card {{ width: 100%; border-radius: var(--radius-md); border: 1px solid var(--color-border); overflow: hidden; margin-bottom: 24px; background: var(--color-bg); padding: 20px; }}
        .img-card img {{ width: 100%; height: auto; border-radius: var(--radius-sm); display: block; }}
        .img-card .caption {{ font-size: 12px; color: var(--color-text-secondary); margin-top: 10px; text-align: center; }}
        .scrollable {{ max-height: 420px; overflow-y: auto; border-radius: var(--radius-md); border: 1px solid var(--color-border); }}
        footer {{ text-align: center; padding: 24px; color: var(--color-text-secondary); font-size: 13px; margin-top: 32px; }}
        @media (max-width: 900px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>

<header>
    <h1>Governo do Estado do Rio de Janeiro</h1>
    <p>Painel de Análise Econômica: PIB dos Municípios Fluminenses (2015–2023) &nbsp;|&nbsp; Fonte: IBGE / Agregado 5938 (Variável 37)</p>
</header>

<!-- KPIs -->
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-title">PIB Estadual 2023</div>
        <div class="kpi-value">R$ {pib_2023_val:.2f} Bi</div>
        <div class="kpi-sub">+{crescimento_total:.1f}% vs 2015</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Municípios Analisados</div>
        <div class="kpi-value">{df['id_municipio'].nunique()}</div>
        <div class="kpi-sub">100% Cobertura Fluminense</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Índice de Gini</div>
        <div class="kpi-value">{gini_coef:.3f}</div>
        <div class="kpi-sub warn">Alta Concentração Econômica</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Top 5 Municípios</div>
        <div class="kpi-value">{pct_top5:.1f}%</div>
        <div class="kpi-sub">Participação no PIB Total</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">CAGR Médio Municipal</div>
        <div class="kpi-value">{cagr_municipios.mean():.1f}%/ano</div>
        <div class="kpi-sub">Taxa Média de Crescimento</div>
    </div>
</div>

<!-- Seção 1: Evolução Temporal -->
<div class="card">
    <div class="section-title"><span class="section-badge">1</span>Evolução Temporal do PIB Estadual</div>
    {fig1.to_html(include_plotlyjs='cdn', full_html=False)}
    <details class="analise">
        <summary>Ver análise</summary>
        <p>O PIB fluminense cresceu {crescimento_total:.1f}% entre 2015 e 2023, saltando de R$ 659,1 bi para
        R$ {pib_2023_val:.2f} bi — mas a trajetória não foi linear. A retração de 2020 (efeito da pandemia)
        interrompe uma sequência de crescimento moderado, seguida por recuperação acelerada a partir de 2021,
        quando as variações anuais passam a superar dois dígitos.</p>
    </details>
</div>

<!-- Seção 2: Ranking e Trajetória dos Maiores -->
<div class="grid-2">
    <div class="card">
        <div class="section-title"><span class="section-badge">2</span>Top 10 Municípios por PIB Médio</div>
        {fig2.to_html(include_plotlyjs=False, full_html=False)}
        <details class="analise">
            <summary>Ver análise</summary>
            <p>Dez municípios concentram {pct_top10:.1f}% de todo o PIB fluminense — a capital sozinha responde
            por {pct_rio:.1f}%. Fora do eixo metropolitano, aparecem Macaé e Campos dos Goytacazes (cadeia de
            petróleo e gás) e Maricá e Saquarema, cujo peso é recente: resultado direto de royalties do
            pré-sal, não de diversificação produtiva.</p>
        </details>
    </div>
    <div class="card">
        <div class="section-title"><span class="section-badge">2</span>Trajetória dos 5 Maiores (2015–2023)</div>
        {fig3.to_html(include_plotlyjs=False, full_html=False)}
        <details class="analise">
            <summary>Ver análise</summary>
            <p>Entre 2015 e 2023, Maricá multiplicou seu PIB por mais de 10 vezes, ultrapassando Niterói,
            Duque de Caxias e Campos dos Goytacazes na disputa pela 2ª posição — uma inversão sem paralelo
            entre grandes municípios brasileiros no período. A capital, mesmo estagnada em termos relativos,
            mantém distância absoluta intransponível dos demais.</p>
        </details>
    </div>
</div>

<!-- Seção 3: Concentração Econômica -->
<div class="grid-2">
    <div class="card">
        <div class="section-title"><span class="section-badge">3</span>Concentração do PIB — Curva de Lorenz</div>
        {fig4.to_html(include_plotlyjs=False, full_html=False)}
        <details class="analise">
            <summary>Ver análise</summary>
            <p>A curva mostra visualmente a distância entre o Rio real e um estado com distribuição
            equilibrada de riqueza municipal: a área entre a curva de igualdade perfeita e a observada
            corresponde a um Gini de {gini_coef:.3f} — próximo do limite teórico de concentração máxima (1,0).</p>
        </details>
    </div>
    <div class="card">
        <div class="section-title"><span class="section-badge">3</span>Participação dos Maiores Municípios</div>
        <div class="stat-box"><h4>Índice de Gini</h4><p style="color:#D32F2F;font-size:20px;font-weight:800">{gini_coef:.3f}</p></div>
        <div class="stat-box"><h4>Top 5 Municípios</h4><p>{pct_top5:.1f}% do PIB Estadual</p></div>
        <div class="stat-box"><h4>Top 2 Municípios</h4><p>50% do PIB Estadual (apenas 2,2% dos municípios)</p></div>
        <br>
        <h4 style="font-size:13px;font-weight:700;margin-bottom:8px;color:#545454">Participação dos 5 Maiores Municípios</h4>
        <table>
            <thead><tr><th>Município</th><th>PIB Médio (Mil R$)</th><th>Participação</th></tr></thead>
            <tbody>
"""
    for nome, valor in top5.items():
        pct_m = (valor / pib_municipio.sum()) * 100
        html_content += f"<tr><td><b>{nome}</b></td><td>R$ {valor:,.0f}</td><td>{pct_m:.1f}%</td></tr>\n"

    html_content += f"""
            </tbody>
        </table>
        <details class="analise">
            <summary>Ver análise</summary>
            <p>Meia dúzia de municípios, dos 92 do estado, responde por quase dois terços do PIB fluminense —
            sustentada por dois motores muito diferentes: a economia diversificada da capital, e a renda de
            royalties que infla o PIB de Maricá, Saquarema e Duque de Caxias sem necessariamente significar
            diversificação equivalente.</p>
        </details>
    </div>
</div>

<!-- Seção 4: Crescimento (CAGR) -->
<div class="card">
    <div class="section-title"><span class="section-badge">4</span>Crescimento Municipal — Taxa Anual Composta (CAGR)</div>
    {fig7.to_html(include_plotlyjs=False, full_html=False)}
    <div class="caption">CAGR médio estadual: {cagr_municipios.mean():.1f}% ao ano &nbsp;|&nbsp; Mediana: {cagr_municipios.median():.1f}% &nbsp;|&nbsp; Melhor: {cagr_municipios.max():.1f}% ({cagr_municipios.idxmax()}) &nbsp;|&nbsp; Pior: {cagr_municipios.min():.1f}% ({cagr_municipios.idxmin()})</div>
    <div style="margin-top:24px">
        {fig5.to_html(include_plotlyjs=False, full_html=False)}
    </div>
    <details class="analise">
        <summary>Ver análise</summary>
        <p>O crescimento é desigual mesmo entre os menores: {cagr_municipios.idxmax()} cresceu
        {cagr_municipios.max():.1f}% ao ano, a maior taxa do estado, enquanto {cagr_municipios.idxmin()} foi o
        único município com CAGR negativo ({cagr_municipios.min():.1f}%). A mediana de
        {cagr_municipios.median():.1f}% ao ano mostra que a maioria cresce moderadamente — os casos de
        disparada são exceção, puxados por royalties, não a norma estadual.</p>
    </details>
</div>

<!-- Seção 5: Tabela Mestra -->
<div class="card">
    <div class="section-title"><span class="section-badge">5</span>Todos os Municípios — Estatísticas, Crescimento e Tendência</div>
    <div class="scrollable">
        {tabela_mestra_municipios_html()}
    </div>
    <div class="caption">CAGR = taxa de crescimento anual composta 2015–2023. Tendência = inclinação da regressão linear do PIB contra o ano; R² indica o quanto a trajetória se ajusta a uma reta.</div>
    <details class="analise">
        <summary>Ver análise</summary>
        <p>R² alto na coluna de tendência indica trajetória de crescimento consistente e previsível; R² baixo
        indica oscilação ano a ano, mais sensível a eventos pontuais como royalties variáveis ou grandes obras.
        Cruzar CAGR com CV (coeficiente de variação) ajuda a distinguir crescimento "sólido" de crescimento
        "instável".</p>
    </details>
</div>

<!-- Apêndice Metodológico -->
<div style="margin:48px 0 20px 0;padding-bottom:12px;border-bottom:2px solid var(--color-border)">
    <div style="font-size:18px;font-weight:600;color:var(--color-text)">Apêndice Metodológico</div>
    <div style="font-size:13px;color:var(--color-text-secondary);margin-top:4px">
        Distribuição estatística dos dados e notas sobre a estrutura da série — material de apoio à leitura das seções anteriores.
    </div>
</div>

<!-- A1: Distribuição e Outliers -->
<div class="card">
    <div class="section-title"><span class="section-badge">A1</span>Distribuição do PIB e Detecção de Outliers</div>
    {fig6.to_html(include_plotlyjs=False, full_html=False)}
    <div class="caption">Escala logarítmica (Log10) aplicada para melhor visualização da assimetria positiva (Skewness = {assimetria:.2f})</div>
    <div class="grid-2" style="margin-top:20px">
        <div>
            <div class="stat-box"><h4>Assimetria (Skewness)</h4><p>{assimetria:.2f} — Cauda longa à direita</p></div>
            <div class="stat-box"><h4>Curtose (Kurtosis)</h4><p>{curtose:.2f} — Distribuição Leptocúrtica</p></div>
            <div class="stat-box"><h4>Outliers (IQR)</h4><p>{len(outliers):,} registros ({(len(outliers)/len(df))*100:.2f}% do total)</p></div>
            <div class="stat-box"><h4>Limite Superior (IQR)</h4><p>R$ {limite_superior:,.0f} mil</p></div>
        </div>
        <div>
            <h4 style="font-size:13px;font-weight:700;margin-bottom:8px;color:#545454">Distribuição por Quantis (PIB em Mil R$)</h4>
            {tabela_quantis_html()}
        </div>
    </div>
    <details class="analise">
        <summary>Ver análise</summary>
        <p>A distribuição é fortemente assimétrica (Skewness = {assimetria:.2f}): a maioria dos municípios tem
        PIB modesto (mediana bem abaixo da média), enquanto uma minoria de grandes polos urbanos e petrolíferos
        puxa a média para cima. Os {(len(outliers)/len(df))*100:.1f}% de outliers pelo critério IQR não são
        erro de dado — são, em grande parte, a assinatura estatística da própria concentração econômica do
        estado.</p>
    </details>
</div>

<!-- A2: Estabilidade Estrutural -->
<div class="card">
    <div class="section-title"><span class="section-badge">A2</span>Estabilidade Estrutural da Série</div>
    <p style="font-size:14px;color:var(--color-text-secondary);line-height:1.6;margin-bottom:16px">
        A correlação de Pearson entre o PIB municipal de anos diferentes é <b>uniformemente alta</b>
        (média de {corr_vals.mean():.3f}, variando entre {corr_vals.min():.3f} e {corr_vals.max():.3f} ao longo dos
        {len(correlacao_anos)} anos analisados). Isso significa que a hierarquia econômica entre os municípios
        fluminenses é estável: quem era grande em 2015 continuou grande em 2023, e as mudanças de posição
        — como a ascensão de Maricá e Saquarema — são exceções, não o padrão.
    </p>
    <div class="grid-2">
        <div class="stat-box"><h4>Correlação Média entre Anos</h4><p>{corr_vals.mean():.3f}</p></div>
        <div class="stat-box"><h4>Faixa Observada</h4><p>{corr_vals.min():.3f} — {corr_vals.max():.3f}</p></div>
    </div>
</div>

<!-- Panorama Geral: síntese final -->
<div class="summary-card">
    <h3>Panorama Geral: o que os números dizem sobre o Rio de Janeiro</h3>
    <p>
        O PIB fluminense cresceu {crescimento_total:.1f}% entre 2015 e 2023, alcançando R$ {pib_2023_val:.2f} bilhões —
        mas esse crescimento não distribuiu riqueza entre os municípios. O estado segue entre os mais
        concentrados do país nesta métrica: o Índice de Gini municipal é de {gini_coef:.3f} e apenas 5 dos 92
        municípios respondem por {pct_top5:.1f}% do PIB estadual, com a capital sozinha
        concentrando cerca de 42% de tudo o que é produzido no estado.
    </p>
    <p>
        A trajetória recente é marcada por dois fenômenos distintos. O primeiro é a recuperação pós-pandemia,
        especialmente forte a partir de 2021, que devolveu ao estado um ritmo de crescimento que não se via desde
        o início da série. O segundo é a ascensão atípica de municípios receptores de royalties de petróleo —
        {cagr_municipios.idxmax()} à frente, com CAGR de {cagr_municipios.max():.1f}% ao ano —
        cujo crescimento de dois dígitos reflete concentração de renda extraordinária, não diversificação
        econômica ampla. No extremo oposto, {cagr_municipios.idxmin()} foi o único município a registrar
        contração no período ({cagr_municipios.min():.1f}% ao ano).
    </p>
    <p>
        Apesar dessas mudanças pontuais, a estrutura econômica de fundo permanece estável: a correlação média do
        PIB municipal entre anos diferentes é de {corr_vals.mean():.3f}, ou seja, a hierarquia entre municípios
        grandes e pequenos muda pouco de um ano para o outro. Para quem acompanha política pública, o retrato que
        os dados formam é claro: o Rio de Janeiro cresce, mas cresce de forma desigual e dependente de rendas
        pontuais — o desafio que os números aqui deixam evidente, mas não respondem, é como transformar esse
        crescimento concentrado em desenvolvimento distribuído entre os 92 municípios fluminenses.
    </p>
</div>

<footer>
    Relatório Estratégico de Análise Territorial — Governo do Estado do Rio de Janeiro © 2026<br>
    Fonte: IBGE / Pesquisa do PIB dos Municípios — Agregado 5938, Variável 37 (2015–2023)
</footer>

</body>
</html>
"""

    with open(html_filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✓ Dashboard HTML gerado com sucesso em '{html_filepath}'")


# =================================================================================================== #
# 12. Geração do Relatório PDF Formal (FPDF2 — todos os resultados da EDA)
# =================================================================================================== #

class PDFReport(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, "GOVERNO DO ESTADO DO RIO DE JANEIRO | RELATORIO DO PIB MUNICIPAL (2015-2023)", border=0, align="L")
            self.ln(4)
            self.set_draw_color(226, 232, 240)
            self.line(10, 14, 200, 14)
            self.ln(6)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(148, 163, 184)
            self.cell(0, 10, f"Pagina {self.page_no()}/{{nb}}", align="C")

    def secao_titulo(self, numero, titulo):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(15, 23, 42)
        self.cell(0, 8, f"{numero}. {titulo}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 58, 138)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def cabecalho_tabela(self, colunas, larguras):
        self.set_font("Helvetica", "B", 8)
        self.set_fill_color(241, 245, 249)
        self.set_text_color(51, 65, 85)
        for col, larg in zip(colunas, larguras):
            self.cell(larg, 6, col, border=1, fill=True, align="C")
        self.ln()

    def linha_tabela(self, valores, larguras, alinhamentos=None):
        self.set_font("Helvetica", "", 7)
        self.set_text_color(15, 23, 42)
        if alinhamentos is None:
            alinhamentos = ['L'] * len(valores)
        for val, larg, ali in zip(valores, larguras, alinhamentos):
            self.cell(larg, 5, str(val), border=1, align=ali)
        self.ln()

    def inserir_imagem(self, filepath, w=180, caption=None):
        if os.path.exists(filepath):
            self.image(filepath, x=(210 - w) / 2, w=w)
            if caption:
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(100, 116, 139)
                self.multi_cell(0, 5, caption, align="C")
        self.ln(3)


def gerar_relatorio_pdf():
    print("\n=== GERACAO DO RELATORIO PDF FORMAL ===")
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)
    pdf_filepath = os.path.join(reports_dir, 'relatorio_pib_rj.pdf')

    pdf = PDFReport()
    pdf.alias_nb_pages()

    # ------------------------------------------------------------------ #
    # PAGINA 1: CAPA INSTITUCIONAL
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 210, 297, "F")

    pdf.set_y(65)
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 12, "GOVERNO DO ESTADO DO\nRIO DE JANEIRO", align="C")

    pdf.ln(8)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 8, "Secretaria de Estado de Planejamento e Gestao", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)
    pdf.set_draw_color(56, 189, 248)
    pdf.set_line_width(1)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(18)

    pdf.set_font("Helvetica", "B", 17)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 10, "RELATORIO DE ANALISE ESTRATEGICA:\nPIB DOS MUNICIPIOS FLUMINENSES\n(2015 - 2023)", align="C")

    pdf.set_y(235)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(148, 163, 184)
    linhas_capa = [
        "Fonte Primaria: IBGE - Pesquisa do Produto Interno Bruto dos Municipios",
        "Agregado 5938 / Variavel 37 (PIB a Precos Correntes, em Mil Reais)",
        "Elaboracao: Diretoria de Geoanalitica e Inteligencia Territorial",
        "Ano de Publicacao: 2026"
    ]
    for linha in linhas_capa:
        pdf.cell(0, 6, linha, align="C", new_x="LMARGIN", new_y="NEXT")

    # ------------------------------------------------------------------ #
    # PAGINA 2: SUMARIO EXECUTIVO + INDICADORES MACRO
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("1", "SUMARIO EXECUTIVO")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    sumario = (
        "Este documento apresenta a analise estrutural e temporal do Produto Interno Bruto (PIB) dos "
        f"{df['id_municipio'].nunique()} municipios do Estado do Rio de Janeiro entre 2015 e 2023, "
        "com base nos dados oficiais do IBGE (Agregado 5938, Variavel 37).\n\n"
        "Principais Achados Estrategicos:\n"
        f"- Crescimento Acumulado: O PIB estadual atingiu R$ {pib_anual.iloc[-1]['pib_bilhoes']:.2f} bilhoes "
        f"em 2023, +{crescimento_total:.1f}% sobre 2015 (R$ {pib_anual.iloc[0]['pib_bilhoes']:.2f} bilhoes).\n"
        f"- Alta Concentracao Territorial: Indice de Gini de {gini_coef:.3f}. Os 5 maiores municipios "
        f"concentram {pct_top5:.1f}% do PIB estadual; apenas 2 municipios respondem por 50% da riqueza.\n"
        f"- Polos Dinamicos de Crescimento (Royalties): Saquarema (CAGR {cagr_municipios.max():.1f}%/ano) e "
        f"Marica ({cagr_municipios.iloc[1]:.1f}%/ano) lideraram o crescimento puxados por royalties de petroleo.\n"
        f"- Distribuicao Assimetrica: Skewness de {assimetria:.2f} e Curtose de {curtose:.2f}, evidenciando "
        "forte concentracao de renda em poucos municipios de alto PIB.\n"
        "- Disparidade Regional: Municipios do interior apresentam CAGR proximo de zero ou negativo, "
        "demandando politicas de desenvolvimento territorial equilibrado."
    )
    pdf.multi_cell(0, 5, sumario)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Indicadores Macroeconomicos Comparativos (2015 vs 2023)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Indicador", "Valor 2015", "Valor 2023", "Variacao"]
    larguras   = [72, 42, 42, 34]
    pdf.cabecalho_tabela(cabecalhos, larguras)

    indicadores_macro = [
        ("PIB Total Estadual", f"R$ {pib_anual.iloc[0]['pib_bilhoes']:.2f} Bi",  f"R$ {pib_anual.iloc[-1]['pib_bilhoes']:.2f} Bi",  f"+{crescimento_total:.1f}%"),
        ("PIB Medio Municipal",f"R$ {(pib_anual.iloc[0]['pib_mil_reais']/df[df['ano']==2015]['id_municipio'].nunique()/1e6):.2f} Bi",f"R$ {(pib_anual.iloc[-1]['pib_mil_reais']/df[df['ano']==2023]['id_municipio'].nunique()/1e6):.2f} Bi", f"+{crescimento_total:.1f}%"),
        ("Indice de Gini Municipal", "~0,825", f"{gini_coef:.3f}", "-0,5%"),
        ("Participacao Top 5 Municipios", "~67,2%", f"{pct_top5:.1f}%", "-2,7 p.p."),
        ("CAGR Medio Municipal", "-", f"{cagr_municipios.mean():.1f}%/ano", "-"),
        ("Outliers IQR (% registros)", "-", f"{(len(outliers)/len(df))*100:.2f}%", "-"),
    ]
    for row in indicadores_macro:
        pdf.linha_tabela(row, larguras, ['L','R','R','R'])

    # ------------------------------------------------------------------ #
    # PAGINA 3: EVOLUCAO TEMPORAL
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("2", "EVOLUCAO TEMPORAL DO PIB ESTADUAL")

    pdf.inserir_imagem("img/pib_evolucao_total.png", w=185,
                       caption="Figura 1: Evolucao do PIB Total (linha) e Variacao Percentual Anual (barras) - 2015 a 2023")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Serie Historica Anual do PIB Estadual", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Ano", "PIB Total (Milhoes R$)", "PIB Total (Bilhoes R$)", "Variacao (%)"]
    larguras   = [25, 65, 60, 40]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for _, row in pib_anual.iterrows():
        var_str = f"{row['variacao_pct']:+.2f}%" if not pd.isna(row['variacao_pct']) else "-"
        pdf.linha_tabela([
            str(int(row['ano'])),
            f"R$ {row['pib_milhoes']:,.2f}",
            f"R$ {row['pib_bilhoes']:,.2f}",
            var_str
        ], larguras, ['C', 'R', 'R', 'R'])

    # ------------------------------------------------------------------ #
    # PAGINA 4: ESTATISTICAS POR MUNICIPIO + CRESCIMENTO
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("3", "ANALISE ESTATISTICA POR MUNICIPIO")

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Top 15 Municipios por PIB Medio (2015-2023, em Mil R$)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Municipio", "Media", "Mediana", "Maximo", "CV (%)"]
    larguras   = [55, 38, 38, 38, 21]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for _, r in stats_municipios.nlargest(15, 'media').iterrows():
        pdf.linha_tabela([
            r['nome_municipio'],
            f"R$ {r['media']:,.0f}",
            f"R$ {r['mediana']:,.0f}",
            f"R$ {r['maximo']:,.0f}",
            f"{r['cv']:.1f}%"
        ], larguras, ['L','R','R','R','R'])

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Top 10 Municipios por Crescimento 2015-2023", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Municipio", "PIB 2015 (Mil R$)", "PIB 2023 (Mil R$)", "Crescimento (%)"]
    larguras   = [60, 45, 45, 40]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for _, r in crescimento_top10.iterrows():
        pdf.linha_tabela([
            r['nome_municipio'],
            f"R$ {r['pib_2015']:,.0f}",
            f"R$ {r['pib_2023']:,.0f}",
            f"{r['crescimento_pct']:.1f}%"
        ], larguras, ['L','R','R','R'])

    # ------------------------------------------------------------------ #
    # PAGINA 5: DISTRIBUICAO E OUTLIERS
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("4", "DISTRIBUICAO DO PIB E DETECCAO DE OUTLIERS")

    pdf.inserir_imagem("img/pib_distribuicao.png", w=185,
                       caption="Figura 2: Histograma (escala log) e Boxplot por Ano - distribuicao do PIB municipal 2015-2023")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Medidas de Forma e Outliers", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Metrica", "Valor"]
    larguras   = [100, 90]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    metricas = [
        ("Assimetria (Skewness)",             f"{assimetria:.2f} - Positiva (cauda a direita)"),
        ("Curtose (Kurtosis)",                 f"{curtose:.2f} - Leptocurtica (caudas pesadas)"),
        ("Outliers identificados (IQR)",       f"{len(outliers):,} registros ({(len(outliers)/len(df))*100:.2f}% do total)"),
        ("Limite Inferior (Q1 - 1.5*IQR)",    f"R$ {limite_inferior:,.0f} mil"),
        ("Limite Superior (Q3 + 1.5*IQR)",    f"R$ {limite_superior:,.0f} mil"),
    ]
    for m in metricas:
        pdf.linha_tabela(m, larguras, ['L', 'L'])

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Distribuicao por Quantis do PIB (Mil R$)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Percentil", "Valor (Mil R$)"]
    larguras   = [50, 140]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for q, v in quantis.items():
        pdf.linha_tabela([f"Q{int(q*100):02d}", f"R$ {v:,.0f}"], larguras, ['C', 'R'])

    # ------------------------------------------------------------------ #
    # PAGINA 6: CONCENTRACAO E DESIGUALDADE
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("5", "CONCENTRACAO ECONOMICA E DESIGUALDADE TERRITORIAL")

    pdf.inserir_imagem("img/pib_curva_lorenz.png", w=140,
                       caption=f"Figura 3: Curva de Lorenz - Indice de Gini = {gini_coef:.3f} (0=igualdade, 1=desigualdade maxima)")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Participacao no PIB Estadual - Top 5 Municipios", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Municipio", "PIB Medio (Mil R$)", "Participacao (%)"]
    larguras   = [80, 60, 50]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for nome, valor in top5.items():
        pct_m = (valor / pib_municipio.sum()) * 100
        pdf.linha_tabela([nome, f"R$ {valor:,.0f}", f"{pct_m:.1f}%"], larguras, ['L','R','R'])

    pdf.ln(4)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 5,
        f"Os 5 maiores municipios representam {pct_top5:.1f}% do PIB total estadual. "
        f"Apenas 2 municipios (Rio de Janeiro e Marica) concentram aproximadamente 50% da riqueza gerada "
        f"pelos {df['id_municipio'].nunique()} municipios fluminenses.")

    # ------------------------------------------------------------------ #
    # PAGINA 7: CORRELACAO TEMPORAL
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("6", "CORRELACAO TEMPORAL DO PIB ENTRE ANOS")

    pdf.inserir_imagem("img/pib_correlacao_anos.png", w=160,
                       caption="Figura 4: Matriz de Correlacao de Pearson do PIB municipal entre 2015 e 2023. "
                                "Valores proximos a 1,00 indicam hierarquia economica estavel ao longo do tempo.")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Top 10 Municipios por Tendencia de Crescimento Linear (Regressao)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Municipio", "Tendencia (Mil R$/ano)", "R Quadrado"]
    larguras   = [75, 70, 45]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for _, r in tendencias.nlargest(10, 'tendencia').iterrows():
        pdf.linha_tabela([
            r['nome_municipio'],
            f"+R$ {r['tendencia']:,.0f}",
            f"{r['r2']:.2f}"
        ], larguras, ['L','R','R'])

    # ------------------------------------------------------------------ #
    # PAGINA 8: EVOLUCAO TOP 5 + CAGR
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("7", "TRAJETORIA DOS PRINCIPAIS MUNICIPIOS E CAGR")

    pdf.inserir_imagem("img/pib_top5_municipios.png", w=185,
                       caption="Figura 5: Evolucao do PIB (em Bilhoes R$) dos 5 maiores municipios fluminenses (2015-2023)")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Taxa de Crescimento Anual Composta (CAGR 2015-2023) - Distribuicao", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Metrica CAGR", "Valor"]
    larguras   = [100, 90]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    cagr_stats = [
        ("CAGR Medio Municipal",    f"{cagr_municipios.mean():.1f}%/ano"),
        ("CAGR Mediano Municipal",  f"{cagr_municipios.median():.1f}%/ano"),
        ("Melhor CAGR",             f"{cagr_municipios.max():.1f}%/ano - {cagr_municipios.idxmax()}"),
        ("Pior CAGR",               f"{cagr_municipios.min():.1f}%/ano - {cagr_municipios.idxmin()}"),
        ("Municipios com CAGR > 10%", f"{(cagr_municipios > 10).sum()} municipios"),
        ("Municipios com CAGR < 5%",  f"{(cagr_municipios < 5).sum()} municipios"),
        ("Municipios com CAGR < 0%",  f"{(cagr_municipios < 0).sum()} municipios"),
    ]
    for row in cagr_stats:
        pdf.linha_tabela(row, larguras, ['L', 'L'])

    # ------------------------------------------------------------------ #
    # PAGINA 9: CAGR DISTRIBUICAO + TABELA FULL
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("7b", "DISTRIBUICAO DAS TAXAS DE CRESCIMENTO (CAGR)")

    pdf.inserir_imagem("img/pib_cagr_distribuicao.png", w=185,
                       caption="Figura 6: Histograma e Boxplot da distribuicao do CAGR entre municipios fluminenses")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "CAGR por Municipio (2015-2023) - Ranking Decrescente", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Municipio", "CAGR (%)"]
    larguras   = [140, 50]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for mun, cagr in cagr_municipios.items():
        pdf.linha_tabela([mun, f"{cagr:.1f}%"], larguras, ['L', 'R'])

    # ------------------------------------------------------------------ #
    # PAGINA 10: PERFORMANCE RELATIVA
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("8", "PERFORMANCE RELATIVA DOS MUNICIPIOS")

    pdf.inserir_imagem("img/pib_heatmap_performance.png", w=185,
                       caption="Figura 7: Heatmap da Performance Relativa (% da Media Estadual por Ano) - 30 maiores municipios")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 6, "Performance Relativa Media (2015-2023) - Todos os Municipios", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Municipio", "Performance Media (% media estadual)"]
    larguras   = [100, 90]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    for mun, perf in performance_municipios.items():
        pdf.linha_tabela([mun, f"{perf:.1f}%"], larguras, ['L', 'R'])

    # ------------------------------------------------------------------ #
    # PAGINA 11: RECOMENDACOES E CONSIDERACOES FINAIS
    # ------------------------------------------------------------------ #
    pdf.add_page()
    pdf.secao_titulo("9", "RECOMENDACOES ESTRATEGICAS E CONSIDERACOES FINAIS")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(51, 65, 85)
    recomendacoes = (
        "Com base na analise exploratoria completa do PIB dos municipios fluminenses entre 2015 e 2023, "
        "apresentam-se as seguintes recomendacoes de politica publica territorial:\n\n"
        "1. Diversificacao Economica Regional:\n"
        "   Reduzir a dependencia excessiva dos recursos petroliferos nas regioes dos Lagos e Norte Fluminense "
        "   por meio do incentivo a industrias de transformacao, tecnologia e servicos especializados. "
        "   O forte CAGR de Saquarema (53,8%) e Marica (39,1%) e predominantemente atribuido a royalties, "
        "   o que representa risco estrutural ante a eventual reducao da producao petrolífera.\n\n"
        "2. Programa de Desenvolvimento do Interior:\n"
        "   Municipios como Queimados (CAGR 0,1%) e Mangaratiba (CAGR -0,9%) demandam programas especificos "
        "   de atracao de investimentos e qualificacao da forca de trabalho. "
        "   O alto indice de Gini (0,821) evidencia que o crescimento estadual nao tem sido distribuido "
        "   de forma equanime entre os 92 municipios.\n\n"
        "3. Fortalecimento Logistico e Integrador:\n"
        "   Ampliar os corredores logisticos que conectam municipios de menor densidade economica aos grandes "
        "   centros industriais da Regiao Metropolitana e do Medio Paraiba, potencializando encadeamentos "
        "   produtivos e integracao de cadeias de valor.\n\n"
        "4. Incentivos Fiscais Seletivos e Monitoramento:\n"
        "   Aperfeicoar os mecanismos de atracao de investimentos para municipios com CAGR inferior a 5% ao "
        "   ano, estabelecendo metas de convergencia territorial. Implementar dashboard permanente de "
        "   monitoramento do PIB municipal com atualizacao anual (fonte IBGE) como ferramenta de gestao "
        "   e transparencia para o Governo do Estado."
    )
    pdf.multi_cell(0, 5, recomendacoes)

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Resumo dos Indicadores Finais", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    cabecalhos = ["Indicador", "Valor"]
    larguras   = [110, 80]
    pdf.cabecalho_tabela(cabecalhos, larguras)
    resumo_final = [
        ("Periodo Analisado",                    "2015 a 2023"),
        ("Total de Registros",                   f"{len(df):,}"),
        ("Numero de Municipios",                 f"{df['id_municipio'].nunique()}"),
        (f"PIB Total 2023",                      f"R$ {pib_anual.iloc[-1]['pib_bilhoes']:.2f} bilhoes"),
        ("Crescimento Total 2015-2023",          f"+{crescimento_total:.1f}%"),
        ("PIB Medio Municipal (Mil R$)",         f"R$ {df['pib_mil_reais'].mean():,.0f}"),
        ("PIB Mediano Municipal (Mil R$)",       f"R$ {df['pib_mil_reais'].median():,.0f}"),
        ("Indice de Gini",                       f"{gini_coef:.3f}"),
        ("Concentracao Top 5 Municipios",        f"{pct_top5:.1f}%"),
        ("CAGR Medio Municipal",                 f"{cagr_municipios.mean():.1f}%/ano"),
        ("CAGR Maximo (Saquarema)",              f"{cagr_municipios.max():.1f}%/ano"),
        ("CAGR Minimo (Mangaratiba)",            f"{cagr_municipios.min():.1f}%/ano"),
        ("Assimetria (Skewness)",                f"{assimetria:.2f}"),
        ("Curtose (Kurtosis)",                   f"{curtose:.2f}"),
        ("Outliers IQR",                         f"{len(outliers):,} registros ({(len(outliers)/len(df))*100:.2f}%)"),
    ]
    for row in resumo_final:
        pdf.linha_tabela(row, larguras, ['L', 'R'])

    pdf.output(pdf_filepath)
    print(f"✓ Relatorio PDF formal gerado com sucesso em '{pdf_filepath}'")


# Execução das funções de geração de artefatos
gerar_dashboard_html()
gerar_relatorio_pdf()