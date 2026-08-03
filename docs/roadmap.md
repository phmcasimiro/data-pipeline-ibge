# Roadmap: Engenharia de Dados & ML com Foco Geoespacial

**Período:** Agosto 2026 – Dezembro 2027 (17 meses ativos + pausa em janeiro 2027)
**Dedicação:** 3 horas líquidas/dia
**Meta salarial:** US$ 7.000–10.000/mês em posição remota internacional

---

## Distribuição diária fixa

| Bloco | Duração | Foco |
|-------|---------|------|
| Bloco 1 | 1h30 | Habilidade técnica principal do mês |
| Bloco 2 | 0h45 | Inglês (speaking prioritário) |
| Bloco 3 | 0h45 | Projeto prático / portfólio / networking |

Essa divisão se mantém durante todo o roadmap. O conteúdo de cada bloco muda conforme a fase.

---

## FASE 1 — Fundação Técnica (Ago–Out 2026)

### Objetivo
Construir a base de engenharia que conecta sua formação geográfica ao mercado tech.

### Mês 1 — Agosto 2026: Python científico + SQL

**Bloco técnico (1h30/dia):**
- Semanas 1–2: Python para dados — NumPy, Pandas (manipulação, limpeza, aggregations). Você provavelmente já viu isso no ADS; o objetivo é fluência, não introdução. Trabalhe com datasets reais (IBGE, INPE).
- Semanas 3–4: SQL do zero ao avançado — JOINs, window functions, CTEs, subqueries. Use PostgreSQL localmente. Pratique no HackerRank SQL ou SQLZoo diariamente.

**Bloco inglês (45min/dia):**
- Speaking é sua prioridade crítica. Use Italki ou Preply para 2–3 aulas semanais de conversação (30min cada). Nos outros dias: shadowing com podcasts técnicos (Syntax.fm, DataFramed). Repita frases em voz alta, grave e ouça.
- Comece a consumir todo conteúdo técnico em inglês a partir de agora. Documentação, tutoriais, Stack Overflow — tudo em inglês.

**Bloco projeto (45min/dia):**
- Configure seu ambiente: GitHub, VS Code, PostgreSQL, ambiente Python.
- Crie o repositório "geo-data-portfolio" no GitHub.
- Primeiro mini-projeto: baixe dados do IBGE (censo, PIB municipal), limpe com Pandas, carregue no PostgreSQL, escreva 10 queries analíticas. Documente em inglês no README.

**Entregável do mês:** Repositório no GitHub com pipeline básico (CSV → limpeza Python → PostgreSQL → análise SQL). README em inglês.

---

### Mês 2 — Setembro 2026: Geoespacial com Python

**Bloco técnico (1h30/dia):**
- Semanas 1–2: GeoPandas + Shapely — leitura de shapefiles, operações espaciais (buffer, intersect, dissolve, spatial joins). Foque em entender GeoDataFrames como extensão natural do Pandas.
- Semanas 3–4: PostGIS — extensão espacial do PostgreSQL. Queries espaciais (ST_Contains, ST_Distance, ST_Buffer, ST_Intersection). Indexação espacial com GiST.

**Bloco inglês (45min/dia):**
- Continue aulas de conversação. Comece a praticar vocabulário técnico: "I built a spatial join pipeline", "the buffer analysis showed that...". Simule explicações de projetos como se estivesse numa entrevista.

**Bloco projeto (45min/dia):**
- Projeto 2: Análise de cobertura de serviços públicos. Use dados do OSM (escolas, hospitais) + malha de setores censitários do IBGE. Calcule áreas atendidas com buffer analysis. Visualize com Folium ou Kepler.gl. Tudo em PostGIS.
- Comece a escrever posts curtos no LinkedIn (em inglês) mostrando o que está construindo. Um post por semana.

**Entregável do mês:** Projeto geoespacial completo com PostGIS, visualização interativa, e README técnico em inglês.

---

### Mês 3 — Outubro 2026: Cloud fundamentals + Git workflow

**Bloco técnico (1h30/dia):**
- Semanas 1–2: AWS fundamentals — S3, IAM, EC2 básico, RDS. Faça o curso gratuito "AWS Cloud Practitioner Essentials". O foco não é a certificação, é entender o ecossistema.
- Semanas 3–4: Docker — containers, Dockerfile, docker-compose. Containerize os projetos que você já fez. Aprenda a rodar PostgreSQL/PostGIS em container.

**Bloco inglês (45min/dia):**
- Aumente as aulas de conversação para 3x/semana. Comece a assistir tech talks no YouTube (re:Invent, PyCon) com legendas em inglês.
- Pratique: descreva seu background em 2 minutos em inglês (elevator pitch). Grave, ouça, refaça.

**Bloco projeto (45min/dia):**
- Suba seus projetos anteriores para rodar em Docker.
- Crie um docker-compose com PostGIS + pgAdmin + sua aplicação Python.
- LinkedIn: continue posts semanais. Comece a seguir e interagir com perfis de GeoAI, geospatial data engineering, remote jobs.

**Entregável do mês:** Projetos anteriores containerizados. Entendimento sólido de AWS core services. Elevator pitch gravado em inglês.

---

## FASE 2 — Especialização (Nov 2026 – Fev 2027)

### Objetivo
Desenvolver skills de engenharia de dados e ML aplicados ao domínio geoespacial.

### Mês 4 — Novembro 2026: Pipelines de dados

**Bloco técnico (1h30/dia):**
- Semanas 1–2: Apache Airflow — DAGs, operators, scheduling, sensors. Instale com Docker, crie pipelines que automatizam seus projetos anteriores (download de dados → processamento → carga no PostGIS).
- Semanas 3–4: dbt (data build tool) — models, tests, documentation. Conecte ao PostgreSQL e crie transformações SQL versionadas dos seus dados geoespaciais.

**Bloco inglês (45min/dia):**
- Foque em escrita técnica: pratique escrever READMEs, documentação de projeto, descrições de pull requests. Use Grammarly para feedback.
- Speaking: simule daily standups — "Yesterday I worked on X, today I'll work on Y, no blockers."

**Bloco projeto (45min/dia):**
- Projeto 3: Pipeline automatizado de monitoramento ambiental. Use dados do INPE (desmatamento DETER/PRODES) ou MapBiomas. Airflow orquestra: download automático → processamento GeoPandas → carga PostGIS → alerta se desmatamento exceder threshold. Documente com dbt.
- Este é o projeto que vai diferenciar você. Capriche.

**Entregável do mês:** Pipeline Airflow funcional com dados geoespaciais reais, documentado com dbt.

---

### Mês 5 — Dezembro 2026: Cloud data stack + Google Earth Engine

**Bloco técnico (1h30/dia):**
- Semanas 1–2: Google Earth Engine (GEE) com Python API. Processamento de imagens de satélite em escala. NDVI, classificação de uso do solo, séries temporais. Seu mestrado em Geografia é vantagem direta aqui.
- Semanas 3–4: BigQuery — data warehouse serverless. Carregue dados geoespaciais, use BigQuery GIS (ST_ functions nativas). Integre com GEE exports.

**Bloco inglês (45min/dia):**
- Comece a fazer mock interviews em inglês. Use Pramp (gratuito) ou peça ao seu tutor do Italki para simular entrevistas técnicas.
- Assista a entrevistas técnicas no YouTube para calibrar expectativas.

**Bloco projeto (45min/dia):**
- Projeto 4: Dashboard de mudanças de uso do solo. GEE processa imagens Sentinel-2 → exporta para BigQuery → visualização com Streamlit ou Deck.gl. Compare cobertura vegetal entre 2 períodos.
- Publique um artigo técnico no Medium ou Dev.to (em inglês) explicando o projeto.

**Entregável do mês:** Projeto GEE + BigQuery publicado. Primeiro artigo técnico em inglês.

---

### Janeiro 2027 — PAUSA (Férias)

Descanse de verdade. Único compromisso: mantenha 20–30min/dia de inglês passivo (séries, podcasts, leitura casual em inglês). Não estude tech.

---

### Mês 7 — Fevereiro 2027: Machine Learning aplicado

**Bloco técnico (1h30/dia):**
- Semanas 1–2: scikit-learn — classificação, regressão, clustering, validação cruzada, feature engineering. Aplique a dados geoespaciais (classificação de uso do solo, predição de preço imobiliário por localização).
- Semanas 3–4: Introdução a deep learning com PyTorch — redes neurais básicas, CNNs para imagens de satélite. Não precisa ir fundo; o foco é entender a arquitetura e saber usar.

**Bloco inglês (45min/dia):**
- Intensifique mock interviews. Pratique explicar conceitos técnicos em inglês: "This model uses a Random Forest classifier to predict land use categories based on spectral bands..."
- Leia papers curtos em inglês sobre GeoAI (Google Scholar: "geospatial machine learning").

**Bloco projeto (45min/dia):**
- Projeto 5: Modelo de classificação de uso do solo usando features geoespaciais. Dados do MapBiomas + variáveis climáticas + topografia. Pipeline completo: coleta → feature engineering → treino → avaliação → deploy com FastAPI.
- Atualize seu LinkedIn com as novas skills.

**Entregável do mês:** Modelo de ML geoespacial deployado com API. Portfólio com 5 projetos.

---

## FASE 3 — Posicionamento Profissional (Mar–Jun 2027)

### Objetivo
Tornar-se visível no mercado internacional e conseguir a primeira posição remota.

### Mês 8 — Março 2027: MLOps + infraestrutura de produção

**Bloco técnico (1h30/dia):**
- Semanas 1–2: MLflow — experiment tracking, model registry, model serving. Integre com seus projetos de ML anteriores.
- Semanas 3–4: CI/CD com GitHub Actions. Testes automatizados (pytest). Terraform básico para infraestrutura como código.

**Bloco inglês (45min/dia):**
- Foque em fluência conversacional. Objetivo: conseguir manter uma conversa técnica de 30 minutos sem travar.
- Comece a participar de comunidades em inglês: Discord de GeoAI, Slack de data engineering (dbt Community, Locally Optimistic).

**Bloco projeto (45min/dia):**
- Refatore seus melhores projetos com boas práticas de produção: testes, CI/CD, documentação, containerização completa.
- Crie um site portfólio simples (GitHub Pages) em inglês consolidando todos os projetos.

**Entregável do mês:** Portfólio profissional online. Projetos com CI/CD. Participação ativa em 2+ comunidades internacionais.

---

### Mês 9 — Abril 2027: LLMs, RAG e dados geoespaciais

**Bloco técnico (1h30/dia):**
- Semanas 1–2: LLMs aplicados — LangChain/LlamaIndex, embeddings, RAG (Retrieval-Augmented Generation). Este é o skill que está pagando mais no mercado agora.
- Semanas 3–4: RAG geoespacial — combine busca semântica com dados espaciais. Exemplo: "Quais áreas de risco de enchente estão próximas de escolas?" usando documentos técnicos + PostGIS.

**Bloco inglês (45min/dia):**
- Conversação diária. Seu speaking deve estar no nível intermediário-alto neste ponto.
- Pratique negociação salarial em inglês: "Based on my experience with geospatial data engineering and the market rate for this role..."

**Bloco projeto (45min/dia):**
- Projeto 6: Assistente de análise geoespacial com RAG. Ingere relatórios ambientais (PDFs) + dados espaciais. Usuário pergunta em linguagem natural, sistema responde com dados e mapa. Deploy com Streamlit.
- Este projeto é ouro para entrevistas. Combina LLM + geoespacial + engenharia.

**Entregável do mês:** Projeto RAG geoespacial funcional. Skill de LLMs demonstrável.

---

### Mês 10 — Maio 2027: Preparação para o mercado internacional

**Bloco técnico (1h30/dia):**
- Semanas 1–2: System design — como projetar sistemas de dados em escala. Estude padrões: batch vs streaming, data lake vs warehouse, event-driven architecture. Leia "Designing Data-Intensive Applications" (capítulos-chave).
- Semanas 3–4: Spark/PySpark básico + Kubernetes básico. Não precisa dominar, mas precisa saber conversar sobre.

**Bloco inglês (45min/dia):**
- Mock interviews intensivas (3x/semana). Simule entrevistas comportamentais (STAR method) e técnicas.
- Grave um vídeo de 3 minutos se apresentando em inglês. Refaça até estar natural.

**Bloco projeto (45min/dia):**
- Reescreva seu currículo em inglês, formato americano (1–2 páginas, sem foto, foco em impacto e métricas).
- Otimize LinkedIn completamente em inglês: headline, about, experiência, projetos.
- Comece a aplicar em plataformas: Arc.dev, Turing, Toptal, WeWorkRemotely, LinkedIn Jobs (remote, geospatial, data engineer).

**Entregável do mês:** CV e LinkedIn prontos. Primeiras 20+ aplicações enviadas.

---

### Mês 11 — Junho 2027: Aplicações intensivas + entrevistas

**Bloco técnico (1h30/dia):**
- Estudo focado em gaps que surgirem das entrevistas. Cada rejeição é informação — anote o que perguntaram e estude.
- Pratique coding challenges leves (LeetCode easy/medium) — muitas empresas pedem, especialmente as americanas.
- Revise SQL avançado e Python para entrevistas.

**Bloco inglês (45min/dia):**
- Mock interviews quase diárias. Foco em clareza e confiança, não perfeição.
- Se possível, faça uma imersão de fim de semana (workshop, meetup online internacional).

**Bloco projeto (45min/dia):**
- Aplique em 5–10 vagas por semana. Personalize cada aplicação.
- Rede de contatos: envie mensagens para hiring managers no LinkedIn. Peça coffee chats de 15 minutos.
- Considere aplicar para posições de US$ 3.000–5.000 como porta de entrada se as de US$ 7.000+ não responderem ainda.

**Entregável do mês:** Pipeline de aplicações ativo. Primeiras entrevistas realizadas.

---

## FASE 4 — Aceleração (Jul–Dez 2027)

### Objetivo
Conseguir e consolidar posição internacional na faixa salarial alvo.

### Meses 12–14 (Jul–Set 2027): Primeira posição + ramp-up

Se ainda não conseguiu uma posição, intensifique as aplicações e considere:
- Freelancing em plataformas (Upwork, Toptal) para construir track record internacional.
- Contratos de curto prazo que pagam menos mas abrem portas.
- Contribuições open-source em projetos geoespaciais (QGIS, GeoServer, Rasterio).

Se já conseguiu, os primeiros 3 meses são cruciais:
- Entregue mais do que esperam. Over-deliver nos primeiros 90 dias.
- Documente tudo que você faz e o impacto gerado.
- Construa relacionamentos com a equipe — isso facilita promoções e referências.

Continue estudando 1–1h30/dia focado em tecnologias que a empresa usa.

### Meses 15–17 (Out–Dez 2027): Consolidação ou salto

Com 3–6 meses de experiência internacional:
- Se está na faixa de US$ 3.000–5.000: comece a buscar a próxima posição na faixa-alvo. Com experiência internacional comprovada, a negociação fica muito mais fácil.
- Se está na faixa-alvo: foque em consolidar, aprender, e se posicionar para sênior.
- Negocie aumento ou busque nova posição armado com métricas de impacto.

---

## Stack técnica consolidada

| Categoria | Tecnologias |
|-----------|------------|
| Linguagens | Python (avançado), SQL (avançado) |
| Geoespacial | PostGIS, GeoPandas, Shapely, Google Earth Engine, Rasterio, GDAL |
| Dados | Pandas, NumPy, Apache Airflow, dbt, Spark (básico) |
| ML/AI | scikit-learn, PyTorch (básico), LangChain, MLflow, RAG |
| Cloud | AWS (S3, RDS, EC2), GCP (BigQuery, GEE, Vertex AI) |
| Infraestrutura | Docker, GitHub Actions, Terraform (básico), Kubernetes (conceitual) |
| Visualização | Streamlit, Deck.gl, Folium, Kepler.gl |
| API | FastAPI |

---

## Portfólio final (6 projetos-chave)

1. **Pipeline de dados censitários** — CSV → Python → PostGIS → análise SQL
2. **Análise de cobertura de serviços** — OSM + IBGE + PostGIS + visualização interativa
3. **Monitoramento ambiental automatizado** — INPE/MapBiomas + Airflow + PostGIS + alertas
4. **Dashboard de uso do solo** — Google Earth Engine + BigQuery + Streamlit
5. **Classificação de uso do solo com ML** — MapBiomas + scikit-learn + FastAPI
6. **Assistente geoespacial com RAG** — LLM + PostGIS + documentos técnicos + Streamlit

---

## Métricas de progresso

| Marco | Quando | Indicador |
|-------|--------|-----------|
| Base técnica sólida | Out 2026 | 2 projetos no GitHub, SQL fluente |
| Especialização geo | Fev 2027 | 4 projetos, GEE + PostGIS + Airflow |
| Speaking intermediário | Mar 2027 | Consegue manter conversa técnica de 30min |
| Portfólio completo | Mai 2027 | 6 projetos, site online, artigo publicado |
| Primeiras entrevistas | Jun 2027 | Aplicando ativamente, fazendo entrevistas |
| Primeira posição remota | Set 2027 | Contratado (mesmo abaixo da faixa-alvo) |
| Faixa-alvo atingida | Dez 2027 | US$ 7.000–10.000/mês |

---

## Recursos recomendados

**Python/Dados:** Python for Data Analysis (Wes McKinney), documentação oficial Pandas/NumPy.

**SQL:** SQLZoo, Mode Analytics SQL Tutorial, HackerRank SQL.

**Geoespacial:** Documentação PostGIS, Google Earth Engine Guides, "Geocomputation with Python" (online gratuito).

**Engenharia de dados:** Fundamentals of Data Engineering (Joe Reis), documentação Airflow e dbt.

**ML:** Hands-On Machine Learning (Aurélien Géron), fast.ai (gratuito).

**System Design:** Designing Data-Intensive Applications (Martin Kleppmann) — capítulos 1–3, 5, 6, 10.

**Inglês speaking:** Italki/Preply (tutores), Elsa Speak (pronúncia), shadowing com podcasts.

**Vagas remotas:** Arc.dev, Turing, Toptal, WeWorkRemotely, RemoteOK, LinkedIn.
