# 🌍 Data Pipeline & Analytics: PIB dos Municípios do Estado do Rio de Janeiro (IBGE)

> **Status:** 🟢 Produção / Pipeline Operacional (Versão v1.0.0)  
> **Arquitetura:** Ingestão Automatizada de API Pública ➔ Modelagem Relacional & DDL ➔ Views Analíticas em PostgreSQL ➔ Estatística Descritiva & Spatial Analytics ➔ Relatórios e Dashboards Executivos.

---

## 📌 Visão Geral do Projeto

Este repositório implementa um **pipeline ponta a ponta de Engenharia e Análise de Dados Econômico-Espaciais**, integrando princípios de **Geografia Quantitativa**, **Modelagem Relacional Avançada** e **Ciência de Dados**.

O fluxo extrai automaticamente a série histórica completa de Produto Interno Bruto (PIB) municipal a preços correntes (2015 a 2023) direto da **API SIDRA do IBGE (Agregado 5938)**, estrutura os dados no formato longo (*Tidy Data*), persiste no banco de dados **PostgreSQL** com schema tipado, chaves primárias e índices analíticos, e calcula métricas avançadas (Índice de Gini, Curva de Lorenz, CAGR e IQR para outliers), exportando um dashboard interativo em HTML e um relatório executivo em PDF.

---

## 🏗️ Arquitetura e Fluxo de Dados

O pipeline foi projetado seguindo o princípio da **Separação de Responsabilidades (Separation of Concerns - SoC)**:

```
                  [ API SIDRA / IBGE v3 ]
                 (Agregado 5938 - Var 37)
                             │
                             ▼  HTTP GET (Requests)
                 [ scripts/etl_pib_ibge.py ]
                             │
                             ▼  Normalização Tidy & Validação
          ┌──────────────────┴──────────────────┐
          │                                     │
          ▼ DDL & Views                         ▼ Truncate & Append
   [ sql/*.sql ]                     [ PostgreSQL: gisdb ]
   - 01_schema.sql                   Schema: geoanalytics
   - 02_views_analytics.sql          Tabela: ibge_pib_municipios_raw
   - 03_queries_relatorio.sql        Views : vw_pib_crescimento_anual
                                             vw_ranking_pib_estadual
                                             vw_resumo_historico_municipios
                                                │
                                                ▼ SQLAlchemy / Pandas / SciPy
                                     [ scripts/analytics.py ]
                                                │
                     ┌──────────────────────────┴──────────────────────────┐
                     ▼                                                     ▼
           [ reports/ & img/ ]                                      [ data/ ]
           - dashboard_pib_rj.html (Plotly)                         - estatisticas_pib_municipios.csv
           - relatorio_pib_rj.pdf (FPDF2)                           - ibge_pib_municipios_raw_*.csv
           - img/*.png (7 Gráficos em 300 DPI)
```

### Componentes da Arquitetura:
1. **Orquestrador Central (`main.py`):** Ponto de entrada unificado que executa sequencialmente o pipeline com monitoramento de tempo, logs formatados e tratamento de exceções.
2. **Camada de Ingestão (`scripts/etl_pib_ibge.py`):** Consome os dados da API pública, normaliza arrays aninhados em formato relacional e aplica os scripts SQL de schema e views antes de realizar a carga.
3. **Camada de Banco de Dados Declarativo (`sql/`):**
   - `01_schema.sql`: DDL declarativo com chave primária composta `(id_municipio, ano)`, tipos estritos e índices `B-Tree`.
   - `02_views_analytics.sql`: Views com **Window Functions** (`LAG()`, `DENSE_RANK()`, `SUM() OVER`) para cálculo de taxas e rankings diretamente no motor do PostgreSQL.
   - `03_queries_relatorio.sql`: Consultas de auditoria de qualidade de dados (*Data Quality*) e rankings prontas para consumo por ferramentas de BI.
4. **Camada Analítica & Visualização (`scripts/analytics.py`):** Cálculos de dispersão, regressão linear, Gini, assimetria, geração de figuras estáticas de alta qualidade, dashboard HTML responsivo e relatório PDF formal.

---

## 🗂️ Estrutura do Repositório

```text
data-pipeline-ibge/
├── data/
│   ├── estatisticas_pib_municipios.csv         # Métricas sumarizadas e KPIs por município
│   └── ibge_pib_municipios_raw_202608021635.csv# Backup local do dataset bruto extraído
│
├── img/                                        # Visualizações estáticas em 300 DPI
│   ├── pib_cagr_distribuicao.png               # Histograma e KDE da taxa composta de crescimento
│   ├── pib_correlacao_anos.png                 # Heatmap de correlação temporal do PIB
│   ├── pib_curva_lorenz.png                    # Curva de Lorenz e Índice de Gini da concentração
│   ├── pib_distribuicao.png                    # Curva de densidade e identificação de cauda longa
│   ├── pib_evolucao_total.png                  # Série temporal do PIB estadual 2015-2023
│   ├── pib_heatmap_performance.png             # Matriz de desempenho relativo municipal
│   └── pib_top5_municipios.png                 # Participação dos 5 maiores municípios
│
├── reports/                                    # Produtos de visualização final
│   ├── dashboard_pib_rj.html                   # Dashboard interativo com componentes Plotly.js
│   └── relatorio_pib_rj.pdf                    # Relatório executivo formal multipágina
│
├── scripts/                                    # Módulos Python executáveis
│   ├── etl_pib_ibge.py                         # Ingestão da API SIDRA e carga no PostgreSQL
│   └── analytics.py                            # Estatística espacial, Gini, gráficos, PDF e HTML
│
├── sql/                                        # Modelagem SQL declarativa e views analíticas
│   ├── 01_schema.sql                           # DDL de criação de schema, tabela e índices B-Tree
│   ├── 02_views_analytics.sql                  # Views com Window Functions (LAG, DENSE_RANK)
│   └── 03_queries_relatorio.sql                # Queries prontas para Data Quality e auditoria
│
├── main.py                                     # Entrypoint: orquestrador do pipeline completo
├── .env.example                                # Modelo de variáveis de ambiente
├── .gitignore                                  # Regras de exclusão do Git (inclui .env e temporários)
├── requirements.txt                            # Dependências Python fixadas
└── README.md                                   # Documentação técnica oficial
```

---

## 🚀 Como Executar o Pipeline Localmente

### Pré-requisitos
- **Python 3.11+** (testado e homologado no Python 3.12/3.14)
- **PostgreSQL 14+** em execução local ou via container
- **Git**

### 1. Clonar o Repositório e Configurar o Ambiente Virtual
```bash
git clone https://github.com/phmcasimiro/data-pipeline-ibge.git
cd data-pipeline-ibge

# Criar ambiente virtual
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Ou no Linux/macOS:
# source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente (`.env`)
Copie o modelo `.env.example` para criar o seu arquivo `.env` local:
```bash
cp .env.example .env
```
Abra o `.env` e preencha com as credenciais do seu banco PostgreSQL:
```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=gisdb
DB_SCHEMA=geoanalytics
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

### 3. Executar o Pipeline Completo (Orquestrador)
Com um único comando, o orquestrador executa a extração, aplica os schemas SQL, carrega o banco e gera todos os artefatos visuais:
```bash
python main.py
```
*Tempo médio de execução: ~25 a 30 segundos.*

---

## 🔍 Verificação de Ambiente e Resultados (Checklist Rápido)

Siga os passos abaixo para auditar se o ambiente e os dados estão corretos:

### Passo 1: Verificar se as Bibliotecas Python estão Prontas
```powershell
python -c "import pandas, numpy, scipy, plotly, fpdf, sqlalchemy, psycopg2; print('-> OK: Todas as dependências prontas!')"
```

### Passo 2: Validar a Conexão com o PostgreSQL e Contagem de Linhas
```powershell
python -c "import os, dotenv, sqlalchemy; dotenv.load_dotenv(); u = os.getenv('DB_USER', 'postgres'); p = os.getenv('DB_PASSWORD', ''); h = os.getenv('DB_HOST', 'localhost'); port = os.getenv('DB_PORT', '5433'); db = os.getenv('DB_NAME', 'gisdb'); e = sqlalchemy.create_engine(f'postgresql+psycopg2://{u}:{p}@{h}:{port}/{db}'); c = e.connect(); r = c.execute(sqlalchemy.text('SELECT count(*) FROM geoanalytics.ibge_pib_municipios_raw')).scalar(); print(f'-> OK: Banco conectado! Total de registros gravados: {r}'); c.close()"
```
- **Esperado:** `-> OK: Banco conectado! Total de registros gravados: 828` (92 municípios fluminenses x 9 anos históricos).

### Passo 3: Conferência Visual dos Produtos Finais
- **Dashboard Interativo:** Abra [`reports/dashboard_pib_rj.html`](reports/dashboard_pib_rj.html) no navegador para explorar gráficos interativos em tela cheia, variação anual e rankings.
- **Relatório Executivo:** Abra [`reports/relatorio_pib_rj.pdf`](reports/relatorio_pib_rj.pdf) para visualizar o documento formal formatado com sumário e tabelas.
- **Figuras Analíticas:** Acesse a pasta [`img/`](img/) para inspecionar os 7 gráficos salvos a 300 DPI.

---

## 📊 Principais Descobertas Econômico-Espaciais (2015–2023)

1. **Hiperconcentração Econômica na Capital:** A Cidade do Rio de Janeiro responde por mais de **42% do PIB estadual acumulado** e mais de **35% em 2023**, atuando como polo centralizador de serviços e capital financeiro.
2. **Alta Desigualdade Territorial (Índice de Gini = 0,821):** O Coeficiente de Gini próximo de 1 atesta extrema concentração da riqueza em poucos municípios litorâneos e da Região Metropolitana, contrastando com vazios econômicos no interior fluminense.
3. **Impacto dos Royalties de Petróleo (Bacia de Campos e Pré-Sal):** Municípios como **Saquarema (+3.032%)**, **Maricá (+1.300%)** e **Arraial do Cabo (+1.064%)** registraram as maiores taxas de crescimento de todo o período, alavancados pela partilha da renda petrolífera.

---

## 👨‍💻 Autor

**Pedro Casimiro**  
*Geógrafo | Analista e Desenvolvedor de Sistemas | Pós-Graduado em Inteligência Artificial*  
- **LinkedIn:** [linkedin.com/in/phmcasimiro](https://linkedin.com/in/phmcasimiro)  
- **GitHub:** [github.com/phmcasimiro](https://github.com/phmcasimiro)  
