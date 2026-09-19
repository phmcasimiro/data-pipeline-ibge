-- =============================================================================
-- SCRIPT DE VIEWS ANALITICAS: Modelagem de Analytics e Window Functions
-- Projeto: Pipeline PIB Municipal (IBGE - RJ)
-- Banco de Dados: PostgreSQL
-- =============================================================================

-- -----------------------------------------------------------------------------
-- View 1: Variação e Crescimento Anual por Município (Uso de LAG Window Function)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW geoanalytics.vw_pib_crescimento_anual AS
WITH pib_lagged AS (
    SELECT 
        id_municipio,
        nome_municipio,
        uf,
        ano,
        pib_mil_reais,
        LAG(pib_mil_reais, 1) OVER (
            PARTITION BY id_municipio 
            ORDER BY ano ASC
        ) AS pib_ano_anterior
    FROM geoanalytics.ibge_pib_municipios_raw
)
SELECT 
    id_municipio,
    nome_municipio,
    uf,
    ano,
    pib_mil_reais,
    pib_ano_anterior,
    (pib_mil_reais - pib_ano_anterior) AS variacao_nominal_mil_reais,
    CASE 
        WHEN pib_ano_anterior IS NOT NULL AND pib_ano_anterior > 0 
        THEN ROUND(((pib_mil_reais::NUMERIC - pib_ano_anterior::NUMERIC) / pib_ano_anterior::NUMERIC) * 100, 2)
        ELSE NULL 
    END AS variacao_percentual_anual
FROM pib_lagged;

-- -----------------------------------------------------------------------------
-- View 2: Ranking Anual e Concentração Estadual (DENSE_RANK e SUM OVER)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW geoanalytics.vw_ranking_pib_estadual AS
WITH totais_estaduais AS (
    SELECT 
        id_municipio,
        nome_municipio,
        uf,
        ano,
        pib_mil_reais,
        DENSE_RANK() OVER (
            PARTITION BY ano 
            ORDER BY pib_mil_reais DESC NULLS LAST
        ) AS ranking_posicao,
        SUM(pib_mil_reais) OVER (
            PARTITION BY ano
        ) AS pib_total_estado_mil_reais
    FROM geoanalytics.ibge_pib_municipios_raw
)
SELECT 
    ano,
    ranking_posicao,
    id_municipio,
    nome_municipio,
    uf,
    pib_mil_reais,
    pib_total_estado_mil_reais,
    ROUND((pib_mil_reais::NUMERIC / pib_total_estado_mil_reais::NUMERIC) * 100, 2) AS participacao_pib_estadual_pct
FROM totais_estaduais;

-- -----------------------------------------------------------------------------
-- View 3: Resumo Estatístico Histórico por Municipio (2015-2023)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW geoanalytics.vw_resumo_historico_municipios AS
SELECT 
    id_municipio,
    nome_municipio,
    uf,
    COUNT(ano) AS anos_observados,
    MIN(pib_mil_reais) AS pib_minimo_mil_reais,
    MAX(pib_mil_reais) AS pib_maximo_mil_reais,
    ROUND(AVG(pib_mil_reais), 0) AS pib_medio_mil_reais,
    ROUND(STDDEV(pib_mil_reais), 0) AS desvio_padrao_mil_reais,
    -- Pega o primeiro e o ultimo PIB disponivel para calculo de crescimento do periodo
    (ARRAY_AGG(pib_mil_reais ORDER BY ano ASC))[1] AS pib_2015,
    (ARRAY_AGG(pib_mil_reais ORDER BY ano DESC))[1] AS pib_2023,
    ROUND(
        (
            ((ARRAY_AGG(pib_mil_reais ORDER BY ano DESC))[1]::NUMERIC - (ARRAY_AGG(pib_mil_reais ORDER BY ano ASC))[1]::NUMERIC) /
            (ARRAY_AGG(pib_mil_reais ORDER BY ano ASC))[1]::NUMERIC
        ) * 100, 2
    ) AS crescimento_acumulado_periodo_pct
FROM geoanalytics.ibge_pib_municipios_raw
GROUP BY id_municipio, nome_municipio, uf;
