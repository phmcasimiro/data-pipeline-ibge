# Pipeline ETL: API IBGE para PostgreSQL

Documentação técnica do script [`data/etl_pib_ibge.py`](../data/etl_pib_ibge.py).

---

## 1. Arquitetura e Fluxo

- **Fonte:** API de Agregados do IBGE (SIDRA v3)
- **Processamento:** Python 3.12 (`requests`, `pandas`, `SQLAlchemy`, `psycopg2`, `python-dotenv`)
- **Destino:** PostgreSQL / PostGIS (`localhost:5433`, banco `gisdb`, schema `geoanalytics`, tabela `ibge_pib_municipios_raw`)

---

## 2. Etapas do ETL

### Extração
- **Endpoint:** `https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2015|2016|2017|2018|2019|2020|2021|2022|2023/variaveis/37?localidades=N6[N3[33]]`
- **Métricas:** Agregado 5938 (PIB Municipal), Variável 37 (PIB a preços correntes em mil R$)
- **Período:** 2015 a 2023
- **Validação:** Verificação HTTP via `response.raise_for_status()`

### Transformação
- **Parsing:** Leitura da estrutura `data[0]['resultados'][0]['series']`
- **Normalização (Formato Longo):** Conversão da série temporal em registros individuais (`id_municipio`, `nome_municipio`, `uf`, `ano`, `pib_mil_reais`)
- **Limpeza de Strings:** Separação de nome e UF por delimitadores `" - "` ou `" (UF)"`
- **Mapeamento de UF:** Mapeamento direto via código IBGE do estado (`id_municipio[:2]`)

### Carga
- **Schema:** Execução de `CREATE SCHEMA IF NOT EXISTS geoanalytics`
- **Persistência:** Ingestão via `pandas.DataFrame.to_sql()` com `if_exists="replace"`

---

## 3. Dicionário de Dados (`geoanalytics.ibge_pib_municipios_raw`)

| Campo | Tipo SQL | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `id_municipio` | `TEXT` | Código IBGE do município (7 dígitos) | `'3300100'` |
| `nome_municipio` | `TEXT` | Nome do município | `'Angra dos Reis'` |
| `uf` | `TEXT` | Sigla da UF | `'RJ'` |
| `ano` | `INTEGER` | Ano de referência | `2015` |
| `pib_mil_reais` | `BIGINT` | Valor do PIB em milhares de Reais | `7600989` |

---

## 4. Execução e Validação

```bash
python data/etl_pib_ibge.py
```

### Consulta de Validação (SQL)
```sql
SELECT * FROM geoanalytics.ibge_pib_municipios_raw ORDER BY ano DESC, pib_mil_reais DESC LIMIT 10;
```
