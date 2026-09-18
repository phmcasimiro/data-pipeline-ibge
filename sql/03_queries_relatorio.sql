-- =============================================================================
-- SCRIPT DE CONSULTAS ANALITICAS & AUDITORIA DE QUALIDADE (DATA QUALITY)
-- Projeto: Pipeline PIB Municipal (IBGE - RJ)
-- Banco de Dados: PostgreSQL
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Validacao de Integridade e Completude (Data Quality Check)
-- Deve retornar exatamente 92 municipios e 828 registros totais (9 anos por municipio)
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_registros,
    COUNT(DISTINCT id_municipio) AS total_municipios,
    COUNT(DISTINCT ano) AS total_anos,
    MIN(ano) AS ano_inicial,
    MAX(ano) AS ano_final,
    COUNT(*) FILTER (WHERE pib_mil_reais IS NULL) AS registros_nulos
FROM geoanalytics.ibge_pib_municipios_raw;

-- -----------------------------------------------------------------------------
-- 2. Top 10 Municipios com Maior PIB Medio Historico (2015-2023)
-- -----------------------------------------------------------------------------
SELECT 
    ranking_medio,
    nome_municipio,
    uf,
    ROUND(pib_medio_mil_reais / 1000000.0, 2) AS pib_medio_bilhoes_reais,
    ROUND(pib_2015 / 1000000.0, 2) AS pib_2015_bilhoes_reais,
    ROUND(pib_2023 / 1000000.0, 2) AS pib_2023_bilhoes_reais,
    crescimento_acumulado_periodo_pct AS crescimento_pct
FROM (
    SELECT 
        DENSE_RANK() OVER (ORDER BY pib_medio_mil_reais DESC) AS ranking_medio,
        nome_municipio,
        uf,
        pib_medio_mil_reais,
        pib_2015,
        pib_2023,
        crescimento_acumulado_periodo_pct
    FROM geoanalytics.vw_resumo_historico_municipios
) top_mun
WHERE ranking_medio <= 10
ORDER BY ranking_medio;

-- -----------------------------------------------------------------------------
-- 3. Top 10 Municipios com Maior Salto Percentual de Crescimento (2015 a 2023)
-- Evidencia o impacto de royalties de petroleo em municipios da Regiao dos Lagos e Norte Fluminense
-- -----------------------------------------------------------------------------
SELECT 
    nome_municipio,
    uf,
    ROUND(pib_2015 / 1000.0, 2) AS pib_2015_milhoes,
    ROUND(pib_2023 / 1000.0, 2) AS pib_2023_milhoes,
    crescimento_acumulado_periodo_pct AS crescimento_total_pct
FROM geoanalytics.vw_resumo_historico_municipios
ORDER BY crescimento_acumulado_periodo_pct DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 4. Concentracao Economica: Participacao do Top 5 Municipios no PIB Estadual em 2023
-- -----------------------------------------------------------------------------
WITH top5_2023 AS (
    SELECT 
        nome_municipio,
        pib_mil_reais,
        participacao_pib_estadual_pct
    FROM geoanalytics.vw_ranking_pib_estadual
    WHERE ano = 2023 AND ranking_posicao <= 5
)
SELECT 
    nome_municipio,
    ROUND(pib_mil_reais / 1000000.0, 2) AS pib_bilhoes,
    participacao_pib_estadual_pct,
    ROUND(SUM(participacao_pib_estadual_pct) OVER (ORDER BY participacao_pib_estadual_pct DESC), 2) AS participacao_acumulada_pct
FROM top5_2023;
