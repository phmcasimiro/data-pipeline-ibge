# Portfólio de Engenharia de Dados Geoespaciais

Uma coleção de projetos ponta a ponta em engenharia de dados focados em análise geoespacial, monitoramento ambiental e sistemas de informação geográfica (SIG). Este portfólio demonstra proficiência em processamento de dados com Python, bancos de dados espaciais, infraestrutura em nuvem e tecnologias geoespaciais.

**Idioma:** Português (Dados e Documentação) | Inglês (Código)

---

## 🎯 Sobre Este Repositório

Este repositório apresenta aplicações práticas dos princípios de engenharia de dados em contextos geoespaciais e ambientais. Cada projeto segue práticas de nível de produção: fluxos de trabalho reproduzíveis, pipelines automatizados, containerização e documentação abrangente.

**Público-alvo:** Engenheiros de dados, profissionais de SIG (GIS) e empresas que trabalham com dados geoespaciais em escala.

---

## 🛠️ Tecnologias Utilizadas (Tech Stack)

| Categoria | Tecnologias |
|----------|---------------|
| **Linguagens** | Python 3.12, SQL (PostgreSQL) |
| **Geoespacial** | GeoPandas, GeoAlchemy, PostGIS, Google Earth Engine, Folium, GDAL |
| **Processamento de Dados** | Pandas, NumPy, Shapely, Rasterio |
| **Bancos de Dados** | PostgreSQL + PostGIS, Google BigQuery, Cloud Storage |
| **Orquestração** | Apache Airflow, dbt |
| **Visualização** | Folium, Kepler.gl, Streamlit |
| **Infraestrutura** | Docker, Docker Compose, AWS (S3, RDS, EC2) |
| **Controle de Versão** | Git, GitHub |
| **DevOps** | GitHub Actions (CI/CD), MLflow |

---

## 📁 Estrutura do Repositório

```
geo-data-portfolio/
├── README.md                          # Este arquivo
├── .gitignore                         # Regras de ignorar do Git
├── requirements.txt                   # Dependências Python
├── docker-compose.yml                 # Stack completa: PostGIS + pgAdmin + app
│
├── projects/
│   ├── 01-ibge-pipeline/              # Projeto 1: Dados do IBGE → PostgreSQL
│   │   ├── notebooks/
│   │   │   ├── 01_data_exploration.ipynb
│   │   │   ├── 02_pandas_cleaning.ipynb
│   │   │   └── 03_sql_analytics.ipynb
│   │   ├── scripts/
│   │   │   ├── load_ibge.py           # Download dos dados de censo do IBGE
│   │   │   ├── transform_data.py      # Processamento com Pandas
│   │   │   └── load_to_postgres.py    # Ingestão no PostgreSQL
│   │   ├── sql/
│   │   │   ├── schema.sql             # Definição das tabelas
│   │   │   ├── analytics_queries.sql  # 10+ consultas analíticas
│   │   │   └── indexes.sql            # Otimização de desempenho
│   │   ├── data/
│   │   │   ├── raw/                   # Arquivos CSV originais do IBGE
│   │   │   └── processed/             # Exportações CSV limpas
│   │   └── README.md                  # Documentação específica do projeto
│   │
│   ├── 02-service-coverage/           # Projeto 2: Análise de cobertura de serviços geoespaciais
│   │   ├── notebooks/
│   │   │   ├── 01_geopandas_exploration.ipynb
│   │   │   ├── 02_postgis_spatial_ops.ipynb
│   │   │   └── 03_visualization.ipynb
│   │   ├── scripts/
│   │   │   ├── osm_downloader.py      # Download de hospitais e escolas do OSM
│   │   │   ├── spatial_analysis.py    # Operações com GeoPandas + PostGIS
│   │   │   └── generate_maps.py       # Visualizações com Folium/Kepler.gl
│   │   ├── sql/
│   │   │   ├── spatial_functions.sql  # ST_Buffer, ST_Intersects, etc.
│   │   │   └── coverage_analysis.sql  # Consultas espaciais complexas
│   │   ├── data/
│   │   │   ├── shapefiles/            # Setores censitários do IBGE
│   │   │   ├── geojson/               # Saídas processadas
│   │   │   └── output_maps/           # Visualizações geradas
│   │   └── README.md
│   │
│   └── 03-environmental-monitoring/   # Projeto 3: Automação INPE/MapBiomas
│       ├── notebooks/
│       ├── dags/                      # DAGs do Airflow
│       │   └── deforestation_monitor.py
│       ├── scripts/
│       ├── sql/
│       ├── data/
│       └── README.md
│
├── infrastructure/
│   ├── Dockerfile                     # Python + libs geoespaciais
│   ├── docker-compose.yml             # PostGIS + pgAdmin + Python
│   ├── requirements.txt                # Versões dos pacotes Python
│   └── .env.example                   # Template de variáveis de ambiente
│
├── tests/                             # Testes unitários e de integração
│   ├── test_data_loading.py
│   ├── test_spatial_operations.py
│   └── conftest.py
│
├── docs/
│   ├── architecture.md                # Visão geral do design do sistema
│   ├── setup_guide.md                 # Instruções de configuração local
│   ├── aws_deployment.md              # Guia de implantação na nuvem (AWS)
│   └── glossary.md                    # Terminologia geoespacial
│
├── .github/workflows/
│   └── ci.yml                         # Pipeline de CI no GitHub Actions
│
├── notebooks/
│   └── exploration/                   # Notebooks de análises ad-hoc
│
└── config/
    ├── postgres_config.yml            # Configuração do banco de dados
    └── logging_config.py              # Configuração de logs
```

---

## 🚀 Início Rápido (Quick Start)

### Pré-requisitos

- **Python 3.11+**
- **PostgreSQL 14+** (ou uso do Docker)
- **Docker & Docker Compose** (recomendado)
- **Git**
- **Mínimo de 4GB de RAM** (para processamento geoespacial)

### Configuração (Local sem Docker)

```bash
# Clonar o repositório
git clone https://github.com/[seu-github]/geo-data-portfolio.git
cd geo-data-portfolio

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar o banco de dados PostgreSQL
createdb geo_analytics

# Habilitar a extensão PostGIS
psql -d geo_analytics -c "CREATE EXTENSION postgis;"

# Executar as migrações/scripts de schema
psql -d geo_analytics < projects/01-ibge-pipeline/sql/schema.sql
```

### Configuração (Docker — Recomendado)

```bash
# Iniciar todos os serviços (PostgreSQL + PostGIS + pgAdmin)
docker-compose up -d

# Acessar o pgAdmin em http://localhost:5050
# Conexão PostgreSQL: postgres:5432

# Executar um projeto
cd projects/01-ibge-pipeline
python scripts/load_ibge.py
python scripts/transform_data.py
python scripts/load_to_postgres.py
```

### Verificar Instalação

```bash
# Verificar ambiente Python
python --version
pip list | grep -E "geopandas|shapely|psycopg2"

# Testar conexão com PostgreSQL/PostGIS
psql -U postgres -d geo_analytics -c "SELECT PostGIS_version();"

# Testar importações no Python
python -c "import geopandas as gpd; import psycopg2; print('✓ Todas as dependências OK')"
```

---

## 📊 Visão Geral dos Projetos

### Projeto 1: Pipeline de Dados do Censo IBGE
**Habilidades:** Pandas, NumPy, SQL, PostgreSQL, Git  
**Duração:** Agosto de 2026  
**Status:** ✅ Concluído

Extração, limpeza e análise dos dados do Censo e PIB municipal do IBGE. O fluxo de dados segue: CSV → Python (Pandas) → PostgreSQL. Inclui mais de 10 consultas SQL analíticas demonstrando funções de janela (window functions), CTEs e agregações.

**Entregáveis principais:**
- Conjunto de dados: PIB municipal e população do IBGE
- Entregas: 2 arquivos CSV (bruto e processado), consultas SQL, repositório GitHub

**Arquivos:**
- `projects/01-ibge-pipeline/README.md` — Documentação completa do projeto
- `projects/01-ibge-pipeline/notebooks/` — Notebooks Jupyter passo a passo
- `projects/01-ibge-pipeline/sql/analytics_queries.sql` — Consultas SQL complexas

**Destaques de código:**
```python
# Exemplo: Carregar dados do IBGE com Pandas
import pandas as pd
df = pd.read_csv('data/raw/ibge_pib.csv', sep=';', encoding='latin-1')
df['pib_per_capita'] = df['pib'] / df['population']
df.to_csv('data/processed/ibge_enriched.csv', index=False)
```

---

### Projeto 2: Análise de Cobertura de Serviços Geoespaciais
**Habilidades:** GeoPandas, PostGIS, Folium, SQL Espacial, OSM  
**Duração:** Setembro de 2026  
**Status:** ✅ Concluído

Análise da cobertura de serviços públicos (hospitais, escolas) em municípios utilizando dados do OpenStreetMap e setores censitários do IBGE. Combina operações vetoriais (GeoPandas) com consultas em banco de dados espacial (PostGIS).

**Entregáveis principais:**
- Mapa interativo em Folium mostrando a acessibilidade aos serviços
- Identificação de "desertos de saúde" (setores a >2km do hospital mais próximo)
- Estatísticas de cobertura por município
- Publicação no GitHub + Artigo no LinkedIn

**Fluxo de trabalho:**
```
Dados OSM → GeoPandas → Junção Espacial no PostGIS → Análise de Buffer → Visualização com Folium
```

**Arquivos:**
- `projects/02-service-coverage/README.md`
- `projects/02-service-coverage/notebooks/01_geopandas_exploration.ipynb`
- `projects/02-service-coverage/scripts/spatial_analysis.py`

**Destaques de código:**
```python
# Exemplo: Junção espacial em PostGIS
SELECT s.id, COUNT(h.id) as nearby_hospitals
FROM census_sectors s
LEFT JOIN hospitals h ON ST_DWithin(s.geom, h.geom, 2000)  -- Raio de 2km
GROUP BY s.id;
```

---

### Projeto 3: Monitoramento Ambiental (Automação de Pipeline)
**Habilidades:** Airflow, Google Earth Engine, BigQuery, dbt, Alertas  
**Duração:** Novembro–Dezembro de 2026  
**Status:** 🔄 Em Andamento

Pipeline automatizado para monitoramento de tendências de desmatamento utilizando dados de satélite do INPE/MapBiomas. O Apache Airflow orquestra: download de dados → processamento → análise → alertas.

**Em breve:** Documentação detalhada

---

## 🗂️ Como Usar Este Repositório

### Para Aprendizado
1. Comece pelo **Projeto 1** para aprender os fundamentos de SQL e Pandas
2. Avance para o **Projeto 2** para operações geoespaciais (GeoPandas + PostGIS)
3. Explore os notebooks individuais em `projects/[X]/notebooks/`

### Para Construção de Portfólio
1. Faça um **Fork** deste repositório
2. Adapte os projetos para sua própria região geográfica ou domínio de interesse
3. Crie **Issues** no GitHub para novas funcionalidades e melhorias
4. Documente seu processo em um blog pessoal ou no Medium

### Para Preparação de Entrevistas
- **Design de Sistemas:** Veja `docs/architecture.md`
- **SQL:** Consulte `projects/01-ibge-pipeline/sql/analytics_queries.sql`
- **Python:** Analise os scripts em `projects/[X]/scripts/`
- **Nuvem:** Consulte `docs/aws_deployment.md`

---

## 📈 Habilidades Demonstradas

### Engenharia de Dados
- [ ] Design e implementação de pipelines ETL
- [ ] Validação de dados e checagem de qualidade
- [ ] Otimização de desempenho (indexação, ajuste de queries)
- [ ] Tratamento de erros e geração de logs
- [ ] Fluxos de trabalho reproduzíveis

### Análise Geoespacial
- [ ] Sistemas de coordenadas e reprojeção (CRS/EPSG)
- [ ] Operações espaciais (buffer, intersecção, sobreposição)
- [ ] Junções espaciais e análise de proximidade
- [ ] Processamento de dados vetoriais e raster
- [ ] Visualização geoespacial

### Bancos de Dados
- [ ] Fundamentos de PostgreSQL
- [ ] Extensão espacial PostGIS
- [ ] Funções de Janela (Window Functions) e CTEs
- [ ] Otimização de índices (B-tree, GiST)
- [ ] Design conceitual de Data Warehouse

### Nuvem & DevOps
- [ ] Serviços principais da AWS (S3, RDS, EC2)
- [ ] Containerização com Docker
- [ ] CI/CD com GitHub Actions
- [ ] Infraestrutura como Código (básico)

### Engenharia de Software
- [ ] Fluxo de trabalho com Git (branches, PRs, commits)
- [ ] Documentação de código
- [ ] Testes e validação
- [ ] Design de APIs (Introdução ao FastAPI)
- [ ] Logging e monitoramento

---

## 💾 Fontes de Dados

Todas as fontes de dados externas são abertas e gratuitas:

| Conjunto de Dados | Fonte | Formato | Frequência de Atualização |
|---------|--------|--------|------------------|
| Setores censitários | [IBGE](https://www.ibge.gov.br/) | Shapefile | Anual |
| PIB Municipal | [IBGE](https://www.ibge.gov.br/) | CSV | Anual |
| População | [IBGE](https://www.ibge.gov.br/) | CSV | Censo (a cada 10 anos) |
| Pontos de interesse | [OpenStreetMap](https://www.openstreetmap.org/) | GeoJSON | Tempo real |
| Desmatamento | [INPE PRODES](http://www.obt.inpe.br/prodes/) | Raster (GeoTIFF) | Anual |
| Índice de vegetação | [MapBiomas](https://mapbiomas.org/) | Raster/Vetor | Anual |

**Nota:** Todos os dados são processados apenas para fins de análise. As fontes originais são citadas na documentação de cada projeto.

---

## 🔧 Fluxo de Desenvolvimento

### Executando um Projeto Localmente

```bash
cd projects/01-ibge-pipeline

# Opção 1: Notebooks Jupyter (exploratório)
jupyter notebook notebooks/01_data_exploration.ipynb

# Opção 2: Scripts Python (produção)
python scripts/load_ibge.py
python scripts/transform_data.py
python scripts/load_to_postgres.py

# Opção 3: Pipeline completo no Docker
docker-compose up --build
```

### Executando Testes

```bash
# Executar testes unitários
pytest tests/ -v

# Executar teste específico
pytest tests/test_spatial_operations.py -v

# Testar com relatório de cobertura
pytest tests/ --cov=projects --cov-report=html
```

### Depuração (Debugging)

```bash
# PostgreSQL: conectar ao banco de dados
psql -U postgres -d geo_analytics

# Python: ativar logs detalhados (verbose)
export LOG_LEVEL=DEBUG
python scripts/load_ibge.py

# Docker: visualizar logs dos containers
docker-compose logs -f postgres
docker-compose exec postgres psql -U postgres -d geo_analytics
```

---

## 📚 Documentação

Guias detalhados estão disponíveis na pasta `docs/`:

- **[setup_guide.md](docs/setup_guide.md)** — Instalação e configuração do ambiente
- **[architecture.md](docs/architecture.md)** — Design do sistema e diagramas de fluxo de dados
- **[aws_deployment.md](docs/aws_deployment.md)** — Implantação na AWS
- **[glossary.md](docs/glossary.md)** — Terminologia de geoprocessamento e engenharia de dados

Cada projeto também possui seu próprio **README.md** contendo:
- Definição do problema e objetivos
- Fontes de dados e dicionário de dados
- Metodologia e abordagem técnica
- Resultados, visualizações e insights
- Como reproduzir a análise

---

## 🤝 Contribuições

Este é um projeto de portfólio pessoal, mas sugestões e melhorias são super bem-vindas!

1. Faça um **Fork** deste repositório
2. Crie uma **Branch** (`git checkout -b feature/sua-funcionalidade`)
3. Faça **Commit** das alterações (`git commit -m "feat: adiciona nova análise"`)
4. Envie a Branch (**Push**) (`git push origin feature/sua-funcionalidade`)
5. Abra um **Pull Request** com uma descrição clara

**Padrão de Código:** Siga as convenções do [PEP 8](https://www.python.org/dev/peps/pep-0008/).

---

## 📞 Contato & Redes Sociais

- **LinkedIn:** [linkedin.com/in/seu-perfil](https://www.linkedin.com/in/seu-perfil)
- **E-mail:** [seu.email@exemplo.com](mailto:seu.email@exemplo.com)
- **Blog:** [Medium](https://medium.com/@seusuario) | [Dev.to](https://dev.to/seusuario)

Sinta-se à vontade para entrar em contato com dúvidas, oportunidades de trabalho ou colaborações!

---

## 📝 Licença

Este projeto está licenciado sob a **Licença MIT** — consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

Você tem liberdade para utilizar este código para fins pessoais, educacionais e comerciais.

---

## 🙏 Agradecimentos

- **Fontes de Dados:** IBGE, INPE, MapBiomas, OpenStreetMap
- **Bibliotecas:** GeoPandas, PostGIS, Folium, Airflow e todo o ecossistema Python de dados
- **Comunidade:** Stack Overflow, discussões do GitHub e a comunidade de GIS open-source

---

## 🎯 Roteiro de Desenvolvimento (Roadmap)

**Concluídos:**
- ✅ Projeto 1: Pipeline de Dados do IBGE
- ✅ Projeto 2: Análise de Cobertura de Serviços
- ✅ Containerização com Docker

**Em Andamento:**
- 🔄 Projeto 3: Monitoramento Ambiental com Airflow
- 🔄 Projeto 4: Classificação de Imagens de Satélite (Google Earth Engine + ML)

**Planejados:**
- ⏳ Projeto 5: Assistente Geoespacial com LLM (RAG)
- ⏳ Projeto 6: Dashboard de Monitoramento em Tempo Real (Streamlit)
- ⏳ Guia de implantação em produção
- ⏳ Servidor de API (FastAPI + Docker)
- ⏳ Testes unitários e pipeline de CI/CD

---

## 📊 Estatísticas do Repositório

- **Projetos:** 3 (1 concluído, 1 em andamento, 1 planejado)
- **Total de linhas de código:** ~2.000+
- **Documentação:** 100% de cobertura
- **Licença:** MIT

---

**Última Atualização:** Agosto de 2026  
**Versão:** 1.0.0  
**Python:** 3.12  
**PostgreSQL:** 14+

---

**Bons estudos e boa exploração! 🌍📊**