# =================================================================================================== #
# 1. Configuração Inicial e Carregamento dos Dados
# =================================================================================================== #

# Importação das bibliotecas
import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import linregress
from dotenv import load_dotenv
from sqlalchemy import create_engine

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
crescimento = crescimento.nlargest(10, 'crescimento_pct')
for _, row in crescimento.iterrows():
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
# 10. Relatório Resumo
# =================================================================================================== #

print("\n=== INÍCIO DO RELATÓRIO RESUMITIVO ===")

# Gerar relatório consolidado
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