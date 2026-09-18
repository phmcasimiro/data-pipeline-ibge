-- =============================================================================
-- SCRIPT DDL: Definicao de Schema, Tabela e Indices de Otimizacao
-- Projeto: Pipeline PIB Municipal (IBGE - RJ)
-- Banco de Dados: PostgreSQL
-- =============================================================================

-- 1. Criacao do Schema dedicado para analytics geoespacial
CREATE SCHEMA IF NOT EXISTS geoanalytics;

-- 2. Criacao da tabela com tipagem estrita e chave primaria composta
-- A chave primaria (id_municipio, ano) garante a integridade dos dados e impede
-- a duplicacao de registros em caso de reexecucao do pipeline ETL.
CREATE TABLE IF NOT EXISTS geoanalytics.ibge_pib_municipios_raw (
    id_municipio VARCHAR(7) NOT NULL,
    nome_municipio VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    ano SMALLINT NOT NULL,
    pib_mil_reais BIGINT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_ibge_pib_municipios PRIMARY KEY (id_municipio, ano)
);

-- 3. Indices para otimizacao de consultas analiticas (B-Tree)
-- Otimiza filtros temporais (WHERE ano = ...) e agrupamentos por ano
CREATE INDEX IF NOT EXISTS idx_pib_ano 
    ON geoanalytics.ibge_pib_municipios_raw (ano);

-- Otimiza buscas e joins por codigo do municipio
CREATE INDEX IF NOT EXISTS idx_pib_municipio 
    ON geoanalytics.ibge_pib_municipios_raw (id_municipio);

-- Indice composto para acelerar series temporais de municipios especificos
CREATE INDEX IF NOT EXISTS idx_pib_municipio_ano 
    ON geoanalytics.ibge_pib_municipios_raw (id_municipio, ano DESC);

-- Comentario explicativo nas tabelas e colunas (Data Catalog / Documentacao no Banco)
COMMENT ON TABLE geoanalytics.ibge_pib_municipios_raw IS 'Tabela estagiaria (raw) contendo dados historicos de PIB a precos correntes extraidos da API SIDRA do IBGE (Agregado 5938, Variavel 37).';
COMMENT ON COLUMN geoanalytics.ibge_pib_municipios_raw.id_municipio IS 'Codigo oficial do IBGE para o municipio (7 digitos).';
COMMENT ON COLUMN geoanalytics.ibge_pib_municipios_raw.pib_mil_reais IS 'Valor do Produto Interno Bruto a precos correntes em milhares de Reais.';
