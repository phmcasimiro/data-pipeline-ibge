# 🌍 Geo Data Engineering & Spatial Analytics: Pipeline PIB Municipal (IBGE - RJ)

> **Status do Projeto:** 🟡 Em Desenvolvimento Ativo (Versão v0.1.0)
> **Foco Atual:** Engenharia de Dados, ETL Automatizado, Análise Exploratória e Geração de Artefatos de Inteligência Econômico-Espacial.

---

## 📌 Visão Geral & Contexto

Este repositório consolida a construção de um pipeline de engenharia e análise de dados focado em variáveis socioeconômicas e dinâmicas territoriais, integrando princípios de **Geografia Quantitativa**, **Arquitetura de Sistemas** e **Data Science**.

Nesta primeira fase funcional, o projeto implementa um fluxo ponta a ponta que extrai dados históricos de Produto Interno Bruto (PIB) municipal direto da API oficial do IBGE (SIDRA), realiza transformações e modelagem relacional, armazena em banco de dados PostgreSQL e executa uma Análise Exploratória de Dados (EDA) avançada — gerando visualizações estatísticas, um dashboard executivo interativo em HTML e um relatório analítico em PDF.

```
       [ IBGE API (SIDRA v3) ]
                  │
                  ▼ (HTTP GET / Requests)
       [ scripts/etl_pib_ibge.py ]
                  │
                  ▼ (Tidy Normalization & Long Format)
       [ PostgreSQL (Schema: geoanalytics) ]
                  │
                  ▼ (SQLAlchemy / Pandas / SciPy)
       [ scripts/eda_refact.py ]
                  │
         ┌────────┴────────────────────┐
         ▼                             ▼
  [ img/*.png ]              [ reports/ ]
  - 7 Gráficos Analíticos   - dashboard_pib_rj.html (Plotly)
                            - relatorio_pib_rj.pdf (FPDF2)
```

---

## 🎯 O que está Implementado até o Momento

### 1. Ingestão e Pipeline ETL (`scripts/etl_pib_ibge.py`)

- **Extração Automatizada:** Consumo direto da API de Agregados do IBGE (Agregado `5938`, Variável `37` — PIB a preços correntes) cobrindo todos os municípios do Estado do Rio de Janeiro entre **2015 e 2023**.
- **Transformação (Tidy Data):** Normalização de payloads JSON aninhados para modelo relacional tabular em formato longo (*long format*), garantindo sanitização de strings e validação dos códigos IBGE de 7 dígitos.
- **Carga Relacional:** Conexão robusta via SQLAlchemy/Psycopg2 com provisionamento dinâmico de schema (`geoanalytics`) e tabela (`ibge_pib_municipios_raw`).

### 2. Análise Exploratória e Métricas Estatísticas (`scripts/eda_refact.py`)

- **Concentração Econômica:** Cálculo da Curva de Lorenz e do **Coeficiente de Gini** para mensurar a desigualdade na distribuição do PIB municipal no território fluminense.
- **Dinâmica Temporal:** Cálculo de taxa de crescimento anual composta (**CAGR**) por município no período 2015–2023.
- **Detecção de Outliers e Assimetria:** Aplicação do método IQR (Intervalo Interquartil), teste de Skewness (assimetria) e Kurtosis (curtose) para caracterizar o peso desproporcional da capital e dos polos petrolíferos (ex: Maricá, Saquarema, Macaé, Caxias).

### 3. Artefatos de Saída e Visualização

- **Dashboard Interativo:** [`reports/dashboard_pib_rj.html`](reports/dashboard_pib_rj.html) gerado com componentes responsivos em Plotly.js, apresentando evolução temporal, variações anuais, rankings e dispersões.
- **Relatório Executivo:** [`reports/relatorio_pib_rj.pdf`](reports/relatorio_pib_rj.pdf) gerado programaticamente via Python (`fpdf2`).
- **Figuras Analíticas em Alta Resolução:** Diretório [`img/`](img/) com 7 gráficos estáticos salvos a 300 DPI (`pib_curva_lorenz.png`, `pib_cagr_distribuicao.png`, `pib_evolucao_total.png`, etc.).

---

## 🗂️ Estrutura do Repositório

```text
data-pipeline-ibge/
├── data/
│   ├── estatisticas_pib_municipios.csv         # Métricas sumarizadas geradas pela análise
│   └── ibge_pib_municipios_raw_202608021635.csv# Backup local do dataset bruto extraído
│
├── img/                                        # Gráficos de alta resolução (PNG 300 DPI)
│   ├── pib_cagr_distribuicao.png
│   ├── pib_correlacao_anos.png
│   ├── pib_curva_lorenz.png
│   ├── pib_distribuicao.png
│   ├── pib_evolucao_total.png
│   ├── pib_heatmap_performance.png
│   └── pib_top5_municipios.png
│
├── notebooks/                                  # Laboratório de exploração e estudos
│   ├── PythonBasico1.ipynb
│   ├── numpy.ipynb
│   ├── numpy_tensor.ipynb
│   └── promptengeneering.ipynb
│
├── reports/                                    # Produtos de visualização final
│   ├── dashboard_pib_rj.html                   # Dashboard interativo completo (Plotly)
│   └── relatorio_pib_rj.pdf                    # Relatório executivo consolidado (PDF)
│
├── scripts/                                    # Código-fonte executável
│   ├── etl_pib_ibge.py                         # Pipeline de extração e carga no Postgres
│   ├── eda.py                                  # Script de análise exploratória preliminar
│   └── eda_refact.py                           # Pipeline analítico consolidado (Gini, Dashboard, PDF)
│
├── .env.example                                # Template de variáveis de ambiente
├── requirements.txt                            # Dependências Python do ambiente
└── README.md                                   # Documentação oficial do projeto
```

---

## 🚀 Como Executar Localmente (Guia Passo a Passo)

### Pré-requisitos
- **Python 3.11+** (recomendado Python 3.12)
- **PostgreSQL 14+** em execução local ou via container
- **Git**

### 1. Clonar o Repositório e Criar o Ambiente Virtual

```bash
git clone https://github.com/phmcasimiro/data-pipeline-ibge.git
cd data-pipeline-ibge

# Criar ambiente virtual
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Ou no Linux/macOS:
# source venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e ajuste suas credenciais de banco:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=gisdb
DB_SCHEMA=geoanalytics
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
```

### 4. Executar o Pipeline ETL

Executa a requisição na API do IBGE, normaliza os registros e popula a tabela no PostgreSQL:

```bash
python scripts/etl_pib_ibge.py
```

*Saída esperada: Confirmação de extração e ~828 registros inseridos em `geoanalytics.ibge_pib_municipios_raw`.*

### 5. Executar a Análise Estatística & Gerador de Relatórios

Executa os cálculos estatísticos e gera os artefatos visuais:

```bash
python scripts/eda_refact.py
```

*Saída gerada:*

- Imagens salvas em `img/`
- Dashboard interativo gerado em `reports/dashboard_pib_rj.html`
- Relatório executivo gerado em `reports/relatorio_pib_rj.pdf`

---

## 🔍 Verificação de Ambiente e Resultados (Guia de Conferência Rápida)

Esta seção foi desenhada para que **qualquer pessoa (mesmo sem experiência técnica)** consiga conferir se tudo está instalado no lugar certo e funcionando como esperado.

Siga os 4 passos de validação abaixo:

### Passo 1: Verificar se as ferramentas do Python estão instaladas
Com o terminal aberto e o ambiente virtual ativado, cole e execute o comando abaixo:
```bash
python -c "import pandas, numpy, scipy, plotly, fpdf, sqlalchemy, psycopg2; print('-> OK: Todas as bibliotecas Python estao instaladas e prontas!')"
```
- **Resultado Esperado:** Mensagem `-> OK: Todas as bibliotecas Python estao instaladas e prontas!`.
- **Se der erro:** Significa que faltou executar `pip install -r requirements.txt` ou o ambiente `venv` não está ativado.

---

### Passo 2: Verificar a conexão com o Banco de Dados e os Dados Salvos
Para testar se o PostgreSQL está ligado e se os dados do IBGE foram gravados com sucesso (sem precisar instalar utilitários externos como `psql`), execute:
```bash
python -c "import os; from dotenv import load_dotenv; from sqlalchemy import create_engine, text; load_dotenv(); e = create_engine(f'postgresql+psycopg2://{os.getenv(\"DB_USER\")}:{os.getenv(\"DB_PASSWORD\")}@{os.getenv(\"DB_HOST\")}:{os.getenv(\"DB_PORT\")}/{os.getenv(\"DB_NAME\")}'); c = e.connect(); r = c.execute(text('SELECT count(*) FROM geoanalytics.ibge_pib_municipios_raw')).scalar(); print(f'-> OK: Banco conectado! Total de registros gravados: {r}'); c.close()"
```
- **Resultado Esperado:** Mensagem `-> OK: Banco conectado! Total de registros gravados: 828` (são 92 municípios fluminenses x 9 anos analisados).
- **Se der erro:** Verifique se o serviço do PostgreSQL está iniciado e se a senha no arquivo `.env` está correta.

---

### Passo 3: Conferência Rápida dos Arquivos Gerados (Checklist Automático)
Execute este comando para checar se todos os relatórios e arquivos de dados foram criados no disco:
```bash
python -c "import os; arquivos = ['reports/dashboard_pib_rj.html', 'reports/relatorio_pib_rj.pdf', 'data/estatisticas_pib_municipios.csv']; faltam = [f for f in arquivos if not os.path.exists(f)]; print('-> OK: Todos os relatorios e dados foram gerados com sucesso!' if not faltam else f'-> Atencao: Arquivos ainda nao encontrados: {faltam}')"
```

---

### Passo 4: Inspeção Visual dos Resultados (Sem Terminal)
Você pode abrir e conferir os produtos finais diretamente no seu computador:

1. **Dashboard Interativo:** Vá até a pasta `reports/` e dê dois cliques no arquivo [`dashboard_pib_rj.html`](reports/dashboard_pib_rj.html). Ele abrirá automaticamente no seu navegador web com gráficos interativos em tela cheia, rankings e cards com indicadores (KPIs).
2. **Relatório Executivo:** Abra o arquivo [`reports/relatorio_pib_rj.pdf`](reports/relatorio_pib_rj.pdf) para visualizar o documento PDF formal pronto para impressão ou compartilhamento.
3. **Galeria de Gráficos:** Abra a pasta [`img/`](img/). Você deverá ver 7 gráficos em formato PNG em alta resolução (300 DPI), incluindo a Curva de Lorenz e o ranking dos maiores municípios.

---

## 📊 Principais Descobertas Econômico-Espaciais (2015–2023)

1. **Hiperconcentração Econômica na Capital:** A Cidade do Rio de Janeiro responde consistentemente por mais de **60% do PIB total** do Estado, atuando como o núcleo primário de serviços e finanças.
2. **Desigualdade Espacial Extrema:** O cálculo do **Coeficiente de Gini** do PIB municipal reflete forte assimetria territorial e concentração de renda tributária em poucos municípios costeiros e metropolitanos.
3. **Efeito Petróleo (Bacia de Campos e Pré-Sal):** Municípios como **Maricá** e **Saquarema** apresentaram as maiores taxas de aceleração de crescimento (CAGRs de destaque), impulsionados pela destinação e partilha de royalties da extração de óleo e gás.

---

## 👨‍💻 Autor

**Pedro Casimiro**
*Geógrafo | Analista e Desenvolvedor de Sistemas | Pós-Graduado em Inteligência Artificial*

- **LinkedIn:** [linkedin.com/in/phmcasimiro](https://linkedin.com/in/phmcasimiro)
- **GitHub:** [github.com/phmcasimiro](https://github.com/phmcasimiro)
