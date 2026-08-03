# Importação das bibliotecas necessárias:
import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Garante saída UTF-8 no terminal Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de Conexão com o PostgreSQL / PostGIS obtidas do .env
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "gisdb")
DB_SCHEMA = os.getenv("DB_SCHEMA", "geoanalytics")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
TABLE_NAME = "ibge_pib_municipios_raw"

# URL da API de Agregados do IBGE para Municípios (N6[all])
# Agregado 5938: PIB dos Municípios
# Variável 37: Produto Interno Bruto a preços correntes (Mil Reais)
# Períodos: 2015 a 2023
api_ibge = "https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2015|2016|2017|2018|2019|2020|2021|2022|2023/variaveis/37?localidades=N6[N3[33]]"

def get_db_engine():
    """Cria e retorna a engine de conexão SQLAlchemy com o banco PostgreSQL."""
    connection_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(connection_url)

def create_schema_if_not_exists(engine, schema_name):
    """Cria o schema no PostgreSQL caso ele ainda não exista."""
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
        conn.commit()

def fetch_and_extract_pib_data():
    """Requisita os dados na API do IBGE e extrai em formato estruturado (Tidy/Long)."""
    print(f"Fazendo requisição à API do IBGE para todos os municípios (2015-2023)...")
    response = requests.get(api_ibge) # requests é uma biblioteca em python que faz requisições HTTP
    response.raise_for_status() # raise_for_status() lança uma exceção para códigos de status HTTP de erro
    data = response.json() # json() é um método que converte a resposta para um dicionário Python
    
    # Navega na hierarquia do JSON (Variável -> Resultados -> Séries) para obter a lista de localidades com seus respectivos valores do PIB
    series = data[0]['resultados'][0]['series']
    rows = [] # rows é uma lista vazia que será preenchida com os dados da API do IBGE
    
    for item in series: # para cada item na lista de séries
        loc_id = item['localidade']['id']         # Código IBGE de 7 dígitos do Município
        loc_nome_raw = item['localidade']['nome']   # Exemplo: "Alta Floresta D'Oeste (RO)"
        
        # Dicionário de fallback para mapear os 2 primeiros dígitos do código IBGE para a UF
        UF_MAP = {
            '11': 'RO', '12': 'AC', '13': 'AM', '14': 'RR', '15': 'PA', '16': 'AP', '17': 'TO',
            '21': 'MA', '22': 'PI', '23': 'CE', '24': 'RN', '25': 'PB', '26': 'PE', '27': 'AL',
            '28': 'SE', '29': 'BA', '31': 'MG', '32': 'ES', '33': 'RJ', '35': 'SP', '41': 'PR',
            '42': 'SC', '43': 'RS', '50': 'MS', '51': 'MT', '52': 'GO', '53': 'DF'
        }
        
        # Separa o nome do município e a sigla da UF (suporta hífen " - " e parênteses "(UF)")
        if " - " in loc_nome_raw:
            partes = loc_nome_raw.rsplit(" - ", 1)
            nome_municipio = partes[0].strip()
            uf = partes[1].strip()
        elif "(" in loc_nome_raw and loc_nome_raw.endswith(")"):
            nome_municipio = loc_nome_raw[:loc_nome_raw.rfind("(")].strip()
            uf = loc_nome_raw[loc_nome_raw.rfind("(")+1:-1].strip()
        else:
            nome_municipio = loc_nome_raw
            uf = UF_MAP.get(loc_id[:2])
            
        # Itera sobre cada ano disponível no dicionário de série temporal
        for ano_str, valor_str in item['serie'].items():
            if valor_str is not None:
                try:
                    pib_val = int(valor_str)
                except ValueError:
                    pib_val = None
            else:
                pib_val = None
                
            rows.append({
                "id_municipio": loc_id,
                "nome_municipio": nome_municipio,
                "uf": uf,
                "ano": int(ano_str),
                "pib_mil_reais": pib_val
            })
            
    df = pd.DataFrame(rows)
    return df

def run_etl():
    """Executa o pipeline ETL: Extração, Transformação e Carga no PostgreSQL."""
    try:
        # 1. Extração e Transformação
        df = fetch_and_extract_pib_data()
        print(f"Dados extraídos com sucesso: {len(df):,} registros no formato longo (anos 2015 a 2023).".replace(",", "."))
        
        # 2. Conexão ao Banco de Dados
        engine = get_db_engine()
        
        # 3. Criação do Schema no PostgreSQL se não existir
        create_schema_if_not_exists(engine, DB_SCHEMA)
        print(f"Schema '{DB_SCHEMA}' verificado/criado com sucesso.")
        
        # 4. Carga dos dados no PostgreSQL
        print(f"Gravando dados na tabela '{DB_SCHEMA}.{TABLE_NAME}' no banco '{DB_NAME}' ({DB_HOST}:{DB_PORT})...")
        df.to_sql(
            name=TABLE_NAME,
            con=engine,
            schema=DB_SCHEMA,
            if_exists="replace",
            index=False
        )
        print(f"Sucesso! {len(df):,} registros inseridos na tabela '{DB_SCHEMA}.{TABLE_NAME}'.".replace(",", "."))
        
        # 5. Exibe amostragem dos dados inseridos no terminal
        print("\nAmostra dos dados salvos no banco:")
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        print(df.head(10).to_string(index=False))

    except Exception as e:
        print(f"\n[ERRO no ETL]: {e}")

if __name__ == "__main__":
    run_etl()

