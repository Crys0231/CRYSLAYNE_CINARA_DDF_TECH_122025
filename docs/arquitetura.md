# Arquitetura do Projeto – Catálogo Técnico de Rolamentos com Data App Inteligente

## 1. Visão Geral

Este projeto tem como objetivo construir uma solução de dados ponta a ponta que integra **catálogo técnico de rolamentos**, **dados de vendas**, **dados de clientes** e uma **camada inteligente de análise**, permitindo:

* Análises descritivas (vendas, clientes e geografia)
* Comparação de custo e oportunidade para clientes industriais
* Consulta em **linguagem natural** sobre problemas em máquinas industriais
* Recomendação de produtos baseada em similaridade e contexto do problema

A arquitetura segue uma abordagem **modular, escalável e orientada a dados**, inspirada em boas práticas de **Data Engineering + Analytics + ML + LLM Apps**.

---

## 2. Arquitetura em Camadas

A solução está organizada em **cinco camadas principais**:

```
[ Fontes de Dados ]
        ↓
[ Data Lake (Raw / Trusted / Refined) ]
        ↓
[ Feature Engineering & ML ]
        ↓
[ Data App / LLM Interface ]
        ↓
[ Usuário Final ]
```

---

## 3. Camada de Fontes de Dados

### 3.1 Tipos de Dados

* **Produtos (Catálogo Técnico)**

  * Tipo de rolamento
  * Aplicação industrial
  * Capacidade, carga, rotação
  * Preço e custo
  * Problemas comuns associados

* **Vendas**

  * Produto vendido
  * Cliente
  * Data
  * Quantidade
  * Valor

* **Clientes**

  * Segmento industrial
  * Localização geográfica
  * Tipo de máquina
  * Histórico de compras

### 3.2 Formato Inicial

* `products_raw.json`
* `sales_raw.csv`
* `customers_raw.csv`

Esses dados representam a **zona raw**, sem tratamento.

---

## 4. Camada de Data Lake

O Data Lake é organizado em três zonas, seguindo o padrão **medallion architecture**.

### 4.1 Raw Zone (`/data/raw`)

* Dados brutos
* Sem validação ou transformação
* Apenas ingestão

Objetivo: **preservar a fonte original**.

---

### 4.2 Trusted Zone (`/data/trusted`)

* Limpeza de dados
* Padronização de tipos
* Tratamento de valores nulos
* Regras básicas de qualidade

Formato otimizado:

* `.parquet`

Arquivos:

* `products_trusted.parquet`
* `sales_trusted.parquet`
* `customers_trusted.parquet`

Objetivo: **dados confiáveis para análise**.

---

### 4.3 Refined Zone (`/data/refined`)

Modelagem analítica (star schema):

* `dim_product`
* `dim_customer`
* `fact_sales`

Essa camada é usada para:

* Dashboards
* Análises exploratórias
* Data App

Objetivo: **alto desempenho e semântica de negócio**.

---

## 5. Camada de Feature Engineering e Machine Learning

Essa camada conecta dados estruturados com **inteligência semântica**.

### 5.1 Feature Engineering com LLM

Notebook:

* `03_llm_feature_engineering.ipynb`

Atividades:

* Criação de descrições textuais dos produtos
* Associação entre tipos de problemas e aplicações
* Enriquecimento semântico do catálogo

---

### 5.2 Modelo de Similaridade

Notebook:

* `05_ml_similarity.ipynb`

Abordagem:

* Embeddings de texto (descrição do problema + produto)
* Similaridade vetorial (cosine similarity)
* Ranking de produtos mais adequados

Objetivo:

> Dado um problema descrito em linguagem natural, retornar os produtos mais relevantes.

---

## 6. Camada Analítica e Exploratória

Notebook:

* `04_eda_analysis.ipynb`

Inclui:

* Análise de vendas por região
* Perfil de clientes industriais
* Correlação entre tipo de máquina e produto
* Insights de custo vs oportunidade

Essa camada valida hipóteses e alimenta decisões de negócio.

---

## 7. Data App (Camada de Aplicação)

Diretório:

* `/data_app/app.py`

Funcionalidades:

* Interface para entrada em linguagem natural
* Consulta sobre problemas industriais
* Comparação de custo e oportunidade
* Visualização geográfica de clientes
* Recomendação de produtos

Tecnologias esperadas:

* Python
* Streamlit ou framework similar
* Integração com modelo de embeddings

---

## 8. Orquestração e Documentação

### 8.1 Pipelines

Documento:

* `pipelines/pipeline_etl.md`

Define:

* Fluxo ETL
* Dependências entre notebooks
* Ordem de execução

---

### 8.2 Documentação

* `README.md`: visão geral do projeto
* `arquitetura.md`: este documento
* `modelagem_dados.md`: esquema e regras de negócio
* `planejamento.md`: cronograma e entregas

---

## 9. Considerações Finais

Esta arquitetura foi desenhada para:

* Ser **didática** (portfólio e entrega acadêmica)
* Demonstrar domínio em **Dados, ML e LLMs**
* Permitir evolução futura (ex: API, banco vetorial, cloud)

Ela reflete um projeto realista, com separação clara de responsabilidades e foco em valor de negócio.

Gerado com ChatGPT