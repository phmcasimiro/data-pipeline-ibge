# Geospatial Data Engineering Portfolio

A collection of end-to-end data engineering projects focused on geospatial analysis, environmental monitoring, and geographic information systems. This portfolio demonstrates proficiency in Python data processing, spatial databases, cloud infrastructure, and geospatial technologies.

**Language:** Portuguese (Data) | English (Code & Documentation)

---

## 🎯 About This Repository

This repository showcases practical applications of data engineering principles in geospatial and environmental contexts. Each project follows production-grade practices: reproducible workflows, automated pipelines, containerization, and comprehensive documentation.

**Target audience:** Data engineers, GIS professionals, and companies working with geospatial data at scale.

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|---------------|
| **Languages** | Python 3.12, SQL (PostgreSQL) |
| **Geospatial** | GeoPandas, GeoAlchemy, PostGIS, Google Earth Engine, Folium, GDAL |
| **Data Processing** | Pandas, NumPy, Shapely, Rasterio |
| **Databases** | PostgreSQL + PostGIS, Google BigQuery, Cloud storage |
| **Orchestration** | Apache Airflow, dbt |
| **Visualization** | Folium, Kepler.gl, Streamlit |
| **Infrastructure** | Docker, Docker Compose, AWS (S3, RDS, EC2) |
| **Version Control** | Git, GitHub |
| **DevOps** | GitHub Actions (CI/CD), MLflow |

---

## 📁 Repository Structure

```
geo-data-portfolio/
├── README.md                          # This file
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                 # Full stack: PostGIS + pgAdmin + app
│
├── projects/
│   ├── 01-ibge-pipeline/              # Project 1: IBGE Data → PostgreSQL
│   │   ├── notebooks/
│   │   │   ├── 01_data_exploration.ipynb
│   │   │   ├── 02_pandas_cleaning.ipynb
│   │   │   └── 03_sql_analytics.ipynb
│   │   ├── scripts/
│   │   │   ├── load_ibge.py           # Download IBGE census data
│   │   │   ├── transform_data.py      # Pandas processing
│   │   │   └── load_to_postgres.py    # PostgreSQL ingestion
│   │   ├── sql/
│   │   │   ├── schema.sql             # Table definitions
│   │   │   ├── analytics_queries.sql  # 10+ analytical queries
│   │   │   └── indexes.sql            # Performance optimization
│   │   ├── data/
│   │   │   ├── raw/                   # Original IBGE CSV files
│   │   │   └── processed/             # Cleaned CSV exports
│   │   └── README.md                  # Project-specific documentation
│   │
│   ├── 02-service-coverage/           # Project 2: Geospatial service coverage analysis
│   │   ├── notebooks/
│   │   │   ├── 01_geopandas_exploration.ipynb
│   │   │   ├── 02_postgis_spatial_ops.ipynb
│   │   │   └── 03_visualization.ipynb
│   │   ├── scripts/
│   │   │   ├── osm_downloader.py      # Download hospitals, schools from OSM
│   │   │   ├── spatial_analysis.py    # GeoPandas + PostGIS operations
│   │   │   └── generate_maps.py       # Folium/Kepler.gl visualizations
│   │   ├── sql/
│   │   │   ├── spatial_functions.sql  # ST_Buffer, ST_Intersects, etc.
│   │   │   └── coverage_analysis.sql  # Complex spatial queries
│   │   ├── data/
│   │   │   ├── shapefiles/            # IBGE census sectors
│   │   │   ├── geojson/               # Processed outputs
│   │   │   └── output_maps/           # Generated visualizations
│   │   └── README.md
│   │
│   └── 03-environmental-monitoring/   # Project 3: INPE/MapBiomas automation
│       ├── notebooks/
│       ├── dags/                      # Airflow DAGs
│       │   └── deforestation_monitor.py
│       ├── scripts/
│       ├── sql/
│       ├── data/
│       └── README.md
│
├── infrastructure/
│   ├── Dockerfile                     # Python + geospatial libs
│   ├── docker-compose.yml             # PostGIS + pgAdmin + Python
│   ├── requirements.txt                # Python package versions
│   └── .env.example                   # Environment variables template
│
├── tests/                             # Unit and integration tests
│   ├── test_data_loading.py
│   ├── test_spatial_operations.py
│   └── conftest.py
│
├── docs/
│   ├── architecture.md                # System design overview
│   ├── setup_guide.md                 # Local setup instructions
│   ├── aws_deployment.md              # Cloud deployment guide
│   └── glossary.md                    # Geospatial terminology
│
├── .github/workflows/
│   └── ci.yml                         # GitHub Actions CI pipeline
│
├── notebooks/
│   └── exploration/                   # Ad-hoc analysis notebooks
│
└── config/
    ├── postgres_config.yml            # Database configuration
    └── logging_config.py              # Logging setup
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **PostgreSQL 14+** (or use Docker)
- **Docker & Docker Compose** (recommended)
- **Git**
- **4GB RAM minimum** (for geospatial processing)

### Setup (Local without Docker)

```bash
# Clone repository
git clone https://github.com/[your-github]/geo-data-portfolio.git
cd geo-data-portfolio

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
createdb geo_analytics

# Enable PostGIS extension
psql -d geo_analytics -c "CREATE EXTENSION postgis;"

# Run migrations
psql -d geo_analytics < projects/01-ibge-pipeline/sql/schema.sql
```

### Setup (Docker — Recommended)

```bash
# Start all services (PostgreSQL + PostGIS + pgAdmin)
docker-compose up -d

# Access pgAdmin at http://localhost:5050
# PostgreSQL connection: postgres:5432

# Run a project
cd projects/01-ibge-pipeline
python scripts/load_ibge.py
python scripts/transform_data.py
python scripts/load_to_postgres.py
```

### Verify Installation

```bash
# Check Python environment
python --version
pip list | grep -E "geopandas|shapely|psycopg2"

# Test PostgreSQL connection
psql -U postgres -d geo_analytics -c "SELECT PostGIS_version();"

# Test Python imports
python -c "import geopandas as gpd; import psycopg2; print('✓ All dependencies OK')"
```

---

## 📊 Projects Overview

### Project 1: IBGE Census Data Pipeline
**Skills:** Pandas, NumPy, SQL, PostgreSQL, Git  
**Duration:** August 2026  
**Status:** ✅ Complete

Extract, clean, and analyze Brazilian census data (IBGE). Data flows from CSV → Python (Pandas) → PostgreSQL. Includes 10+ analytical SQL queries demonstrating window functions, CTEs, and aggregations.

**Key outputs:**
- Dataset: IBGE municipal PIB and population
- Delivery: 2 CSV files (raw & processed), SQL queries, GitHub repository

**Files:**
- `projects/01-ibge-pipeline/README.md` — Full project documentation
- `projects/01-ibge-pipeline/notebooks/` — Step-by-step Jupyter notebooks
- `projects/01-ibge-pipeline/sql/analytics_queries.sql` — Complex SQL queries

**Technology highlights:**
```python
# Example: Load IBGE data with Pandas
import pandas as pd
df = pd.read_csv('data/raw/ibge_pib.csv', sep=';', encoding='latin-1')
df['pib_per_capita'] = df['pib'] / df['population']
df.to_csv('data/processed/ibge_enriched.csv', index=False)
```

---

### Project 2: Geospatial Service Coverage Analysis
**Skills:** GeoPandas, PostGIS, Folium, Spatial SQL, OSM  
**Duration:** September 2026  
**Status:** ✅ Complete

Analyze coverage of public services (hospitals, schools) across municipalities using OpenStreetMap data and IBGE census sectors. Combines vector operations (GeoPandas) with spatial database queries (PostGIS).

**Key outputs:**
- Interactive Folium map showing service accessibility
- "Healthcare desert" identification (sectors >2km from nearest hospital)
- Coverage statistics by municipality
- GitHub publication + LinkedIn article

**Workflow:**
```
OSM Data → GeoPandas → PostGIS Spatial Join → Buffer Analysis → Folium Visualization
```

**Files:**
- `projects/02-service-coverage/README.md`
- `projects/02-service-coverage/notebooks/01_geopandas_exploration.ipynb`
- `projects/02-service-coverage/scripts/spatial_analysis.py`

**Technology highlights:**
```python
# Example: Spatial join in PostGIS
SELECT s.id, COUNT(h.id) as nearby_hospitals
FROM census_sectors s
LEFT JOIN hospitals h ON ST_DWithin(s.geom, h.geom, 2000)  -- 2km radius
GROUP BY s.id;
```

---

### Project 3: Environmental Monitoring (Pipeline Automation)
**Skills:** Airflow, Google Earth Engine, BigQuery, dbt, Alerts  
**Duration:** November–December 2026  
**Status:** 🔄 In Progress

Automated pipeline monitoring deforestation trends using INPE/MapBiomas satellite data. Apache Airflow orchestrates: data download → processing → analysis → alerting.

**Coming soon:** Detailed documentation

---

## 🗂️ How to Use This Repository

### For Learning
1. Start with **Project 1** for SQL and Pandas fundamentals
2. Move to **Project 2** for geospatial operations (GeoPandas + PostGIS)
3. Explore individual notebooks in `projects/[X]/notebooks/`

### For Portfolio Building
1. Fork this repository
2. Adapt projects to your own geographic area/domain
3. Create Issues on GitHub for features/improvements
4. Document your process in a personal blog or Medium

### For Interview Preparation
- **System design:** See `docs/architecture.md`
- **SQL:** Check `projects/01-ibge-pipeline/sql/analytics_queries.sql`
- **Python:** Review scripts in `projects/[X]/scripts/`
- **Cloud:** Reference `docs/aws_deployment.md`

---

## 📈 Skills Demonstrated

### Data Engineering
- [ ] ETL pipeline design and implementation
- [ ] Data validation and quality checks
- [ ] Performance optimization (indexing, query tuning)
- [ ] Error handling and logging
- [ ] Reproducible workflows

### Geospatial Analysis
- [ ] Coordinate systems and reprojection (CRS/EPSG)
- [ ] Spatial operations (buffer, intersect, overlay)
- [ ] Spatial joins and proximity analysis
- [ ] Vector and raster data processing
- [ ] Geospatial visualization

### Databases
- [ ] PostgreSQL fundamentals
- [ ] PostGIS spatial extensions
- [ ] Window functions and CTEs
- [ ] Index optimization (B-tree, GiST)
- [ ] Data warehouse design (conceptual)

### Cloud & DevOps
- [ ] AWS core services (S3, RDS, EC2)
- [ ] Docker containerization
- [ ] CI/CD with GitHub Actions
- [ ] Infrastructure as Code (basic)

### Software Engineering
- [ ] Git workflow (branches, PRs, commits)
- [ ] Code documentation
- [ ] Testing and validation
- [ ] API design (FastAPI intro)
- [ ] Logging and monitoring

---

## 💾 Data Sources

All external data sources are open and freely available:

| Dataset | Source | Format | Update Frequency |
|---------|--------|--------|------------------|
| Census sectors | [IBGE](https://www.ibge.gov.br/) | Shapefile | Annual |
| Municipal PIB | [IBGE](https://www.ibge.gov.br/) | CSV | Annual |
| Population | [IBGE](https://www.ibge.gov.br/) | CSV | Census (every 10 years) |
| Points of interest | [OpenStreetMap](https://www.openstreetmap.org/) | GeoJSON | Real-time |
| Deforestation | [INPE PRODES](http://www.obt.inpe.br/prodes/) | Raster (GeoTIFF) | Annual |
| Vegetation index | [MapBiomas](https://mapbiomas.org/) | Raster/Vector | Annual |

**Note:** All data is processed for analysis only. Original sources are cited in each project's documentation.

---

## 🔧 Development Workflow

### Running a Project Locally

```bash
cd projects/01-ibge-pipeline

# Option 1: Jupyter notebooks (exploratory)
jupyter notebook notebooks/01_data_exploration.ipynb

# Option 2: Python scripts (production)
python scripts/load_ibge.py
python scripts/transform_data.py
python scripts/load_to_postgres.py

# Option 3: Full pipeline in Docker
docker-compose up --build
```

### Testing

```bash
# Run unit tests
pytest tests/ -v

# Run specific test
pytest tests/test_spatial_operations.py -v

# Test with coverage
pytest tests/ --cov=projects --cov-report=html
```

### Debugging

```bash
# PostgreSQL: connect to database
psql -U postgres -d geo_analytics

# Python: enable verbose logging
export LOG_LEVEL=DEBUG
python scripts/load_ibge.py

# Docker: view logs
docker-compose logs -f postgres
docker-compose exec postgres psql -U postgres -d geo_analytics
```

---

## 📚 Documentation

Detailed guides are available in the `docs/` folder:

- **[setup_guide.md](docs/setup_guide.md)** — Installation and environment setup
- **[architecture.md](docs/architecture.md)** — System design and data flow diagrams
- **[aws_deployment.md](docs/aws_deployment.md)** — Deploying to AWS
- **[glossary.md](docs/glossary.md)** — Geospatial and data engineering terminology

Each project also has its own **README.md** with:
- Problem statement and objectives
- Data sources and data dictionary
- Methodology and technical approach
- Results, visualizations, and insights
- How to reproduce the analysis

---

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

1. **Fork** this repository
2. **Create a branch** (`git checkout -b feature/your-feature`)
3. **Commit changes** (`git commit -m "feat: add new analysis"`)
4. **Push to branch** (`git push origin feature/your-feature`)
5. **Open a Pull Request** with a clear description

**Code style:** Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards.

---

## 📞 Contact & Social

- **LinkedIn:** [linkedin.com/in/your-profile](https://www.linkedin.com/in/your-profile)
- **Email:** [your.email@example.com](mailto:your.email@example.com)
- **Blog:** [Medium](https://medium.com/@yourusername) | [Dev.to](https://dev.to/yourusername)

Feel free to reach out with questions, job inquiries, or collaboration opportunities!

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use this code for personal, educational, and commercial purposes.

---

## 🙏 Acknowledgments

- **Data sources:** IBGE, INPE, MapBiomas, OpenStreetMap
- **Libraries:** GeoPandas, PostGIS, Folium, Airflow, and the entire Python data ecosystem
- **Community:** Stack Overflow, GitHub discussions, and the open-source GIS community

---

## 🎯 Roadmap

**Completed:**
- ✅ Project 1: IBGE Data Pipeline
- ✅ Project 2: Service Coverage Analysis
- ✅ Docker containerization

**In Progress:**
- 🔄 Project 3: Environmental Monitoring with Airflow
- 🔄 Project 4: Satellite Imagery Classification (Google Earth Engine + ML)

**Planned:**
- ⏳ Project 5: LLM-powered Geospatial Assistant (RAG)
- ⏳ Project 6: Real-time Monitoring Dashboard (Streamlit)
- ⏳ Production deployment guide
- ⏳ API server (FastAPI + Docker)
- ⏳ Unit tests and CI/CD pipeline

---

## 📊 Repository Stats

- **Projects:** 3 (1 complete, 1 in progress, 1 planned)
- **Total lines of code:** ~2,000+
- **Documentation:** 100% coverage
- **Last updated:** [Your date]
- **License:** MIT

---

**Last Updated:** August 2026  
**Version:** 1.0.0  
**Python:** 3.12 
**PostgreSQL:** 14+

---

**Happy exploring! 🌍📊**