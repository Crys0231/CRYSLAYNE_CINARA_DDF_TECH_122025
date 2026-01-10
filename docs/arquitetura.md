# Arquitetura do Projeto – Catálogo Técnico de Rolamentos com Data App Inteligente

**Data:** 08/01/2026  
**Status:** Em Produção  

---

## 1. Visão Geral

Este projeto implementa uma **solução completa de data engineering** que integra catálogo técnico de rolamentos, dados de vendas e clientes industriais com pipelines de qualidade, transformação e feature engineering.

**A solução entrega:**

**Data Lakehouse**: 3 camadas (Raw, Trusted, Refined) com arquitetura medallion  
**Data Quality**: Validações automáticas com Soda Core + regras de negócio  
**Transformação**: Padronização de tipos, correção de margens, enriquecimento  
**Feature Engineering**: Descrições técnicas, tags categóricas, matching de problemas  
**Análise Exploratória**: EDA completa com 50+ visualizações e insights  
**Documentação Completa**: Trabalhado desde o começo do projeto 

A arquitetura segue boas práticas de **Data Engineering**, **Data Quality**, **Analytics** e **MLOps**.

---

## 2. Arquitetura em Camadas

```
[ Dados Brutos: JSON + CSV ]
        ↓
[ RAW ZONE: Ingestão (sem transformação) ]
        ↓
[ TRUSTED ZONE: Limpeza + Validação + Transformação ]
        ↓
[ REFINED ZONE: Modelagem Analítica + Features ]
        ↓
[ ANALYTICS LAYER: EDA + Insights + Documentação ]
```

---

## 3. Camada de Fontes de Dados

### 3.1 Dados de Entrada

**PRODUCTS_RAW.JSON** (10.000 registros)
- product_id: P00001 → P10000
- Tipos de rolamento, material, fabricante
- Capacidade de carga, velocidade máxima, limite de temperatura
- Problema que resolve (Vibração, Desgaste, Superaquecimento, Contaminação, Corrosão)
- Preço de venda (list_price) e custo (unit_cost)

**CUSTOMERS_RAW.CSV** (5.000 registros)
- customer_id: C00001 → C05000
- Segmento industrial (8 setores): Química, Automotiva, Alimentos, Mineração, Papel e Celulose, Siderurgia, Energia, Cimento
- Porte (Pequena, Média, Grande)
- Modelo de manutenção (Interna, Terceirizada, Mista)
- Criticidade de equipamentos (Baixa, Média, Alta)
- Orçamento anual, custo de downtime
- Relacionamento desde 2000-2024

**SALES_RAW.CSV** (120.000 registros)
- sale_id: S0000001 → S0150000
- Data, cliente, produto, quantidade
- Preço unitário, total, desconto
- Canal de venda (Direct, Distributor, Representative)
- Tipo de contrato (Spot, Recurring, SLA)
- Período: 2023-2025

---

## 4. Raw Zone (`/data/raw/`)

**Objetivo**: Preservar fonte original sin alteración

**Arquivos:**
- `products_raw.json` (10.000 registros × 14 campos)
- `customers_raw.csv` (5.000 registros × 13 campos)
- `sales_raw.csv` (120.000 registros × 14 campos)

**Características:**
- Sem validação
- Sem transformação
- Apenas ingestão
- Formato original mantido

---

## 5. Trusted Zone (`/data/trusted/`)

**Objetivo**: Dados confiáveis para análise

**Processamento:**

### 5.1 Data Quality (Notebook 02)

**Validações Realizadas:**

**Completude**: 100% de dados completos em todas 3 tabelas  
**Tipo de Dados**: Conversão e padronização  
**Chaves Primárias**: Integridade de customer_id, product_id, sale_id  
**Regras de Negócio**:
- Orçamento de manutenção ≥ 0
- Custo de downtime ≥ 0
- Datas de relacionamento ≤ hoje
- **Detectado:** 359 produtos com margem negativa (unit_cost ≥ list_price)

**Saídas:**
- `customers_trusted.parquet` (5.000 registros)
- `products_trusted.parquet` (10.000 registros)
- `sales_trusted.parquet` (120.000 registros)

### 5.2 Data Transformation (Notebook 03)

**Transformações:**

**PRODUCTS_TRUSTED:**
- Tipos padronizados (float64, int64)
- 359 margens negativas corrigidas (margem mínima = 25%)
- Campo adicionado: `technical_description` (descrição técnica textual)
- Campo adicionado: `technical_features` (tags de características)
- Campo adicionado: `llm_product_description` (versão enriquecida)

**CUSTOMERS_TRUSTED:**
- Tipos padronizados
- Mapeamento de problemas por indústria
- Campo adicionado: `expected_problems` (array de problemas esperados)

**SALES_TRUSTED:**
- Tipos padronizados (datetime)
- Validação total_price = quantity × unit_price
- Desconto validado ∈ [0, 100]

---

## 6. Refined Zone (`/data/refined/`)

**Objetivo**: Modelagem analítica e features para ML

### 6.1 Feature Engineering (Notebook 04)

**Features Criadas:**

**Products Features:**
- `technical_description`: Texto descritivo do produto
- `supported_problems`: Lista de problemas resolvidos
- Binary features: `problem_vibracao`, `problem_desgaste`, `problem_superaquecimento`, `problem_contaminacao`
- Output: `products_features.parquet`

**Customers Features:**
- `expected_problems`: Array de problemas por indústria
- Binary features: `problem_vibracao`, `problem_desgaste`, `problem_superaquecimento`, `problem_contaminacao`
- Output: `customers_features.parquet`

**Sales Refined:**
- Conversão de datas
- Output: `sales_refined.parquet`

---

## 7. Analytics & Exploratory Layer (Notebook 05)

### 7.1 Análise Exploratória (EDA)

**Seções Implementadas:**

**1. Análise de Produtos**
- Distribuição de tipos de rolamentos (5 categorias)
- Distribuição de materiais (Aço, Aço Inoxidável, Cerâmica)
- Capacidade de carga: média = 24.500N, mediana = 20.900N
- Velocidade máxima: 2.000 - 14.000 RPM
- Limite de temperatura: 82 - 250°C

**2. Análise de Clientes**
- Distribuição por indústria (8 setores equilibrados)
- Distribuição por porte (33% Pequena, 34% Média, 33% Grande)
- Distribuição por criticidade (equilibrada)
- Orçamento anual: média = R$ 2,5M, range = R$ 50K - R$ 5M

**3. Análise de Vendas**
- 120.000 transações em 2,5 anos
- Quantidade média: 20.56 unidades
- Preço unitário médio: R$ 1.542,62
- Total médio por transação: R$ 31.711

**4. Análise de Problemas**
- Distribuição de problemas por indústria
- Matriz: Tipo de Rolamento × Problemas
- Produtos premium: Preço vs Volume

**5. Insights & Recomendações**
- Produtos com baixa performance (identificados)
- Clientes com maior potencial (Top 10)
- Rentabilidade por produto (margens)

---

## 8. Documentação & Datapedia (Executado)

### 8.1 Tabelas Documentadas

**Status**: Estrutura das tabelas na plataforma Dadosfera

**CUSTOMERS_RAW:**
- 5.000 registros, 13 campos
- 4 campos criptografados (27%)
- Company name, revenues, budgets, downtime costs

**PRODUCTS_RAW:**
- 10.000 registros, 14 campos
- 2 campos criptografados (14%)
- Unit cost, list price

**SALES_RAW:**
- 120.000 registros, 14 campos
- 4 campos criptografados (29%)
- Customer ID, unit price, total price, discount

**Criptografia:**
- Algoritmo: AES-256
- Descriptografia: Automática via PostgreSQL
- Auditoria: Todos acessos registrados

---

## 9. Pipeline de Execução

### Ordem de Notebooks

```
01_data_generation.ipynb
   ↓
02_data_quality.ipynb (Soda Core + validações)
   ↓
03_data_transformation.ipynb (Trusted Zone)
   ↓
04_llm_feature_engineering.ipynb (Refined Zone + Features)
   ↓
05_eda_analysis.ipynb (Insights & Visualizações)
   ↓
Outputs: Documentação Datapedia
```

### Dependências

- Pandas, NumPy
- Fastparquet (formato parquet)
- Scikit-learn (features, transformações)
- Matplotlib, Seaborn (visualizações)
- Soda-core (data quality)

---

## 10. Dados de Saída

### Arquivos Gerados

| Arquivo | Camada | Formato | Registros |
|---------|--------|---------|-----------|
| customers_raw.csv | Raw | CSV | 5.000 |
| products_raw.json | Raw | JSON | 10.000 |
| sales_raw.csv | Raw | CSV | 120.000 |
| customers_trusted.parquet | Trusted | Parquet | 5.000 |
| products_trusted.parquet | Trusted | Parquet | 10.000 |
| sales_trusted.parquet | Trusted | Parquet | 120.000 |
| dim_customers.parquet | Refined | Parquet | 5.000 |
| dim_products.parquet | Refined | Parquet | 10.000 |
| fact_sales.parquet | Refined | Parquet | 120.000 | 

---

## 11. Métricas de Qualidade

### Data Quality Score

| Métrica | Valor | Alvo |
|---------|-------|------|
| Completude | 100% | ≥ 99% |
| Duplicatas | 0 | = 0 |
| Integridade FK | 100% | ≥ 99% |
| Regras Negócio | 99,7% | ≥ 99% |
| Consistência Tipo | 100% | ≥ 99% |

### Erros Detectados & Corrigidos

- **359 produtos com margem negativa** → Corrigidos com +25% de margem
- **0 dados faltantes** → 100% completo
- **0 duplicatas** → Integridade mantida

---

## 12. Próximas Fases (Roadmap)

**Fase 6: API REST**
- FastAPI com endpoints para consulta de produtos
- Busca por problema, indústria, preço

**Fase 7: Data App Inteligente**
- Streamlit com interface de consulta
- Matching produto ↔ problema
- Recomendações por cliente

**Fase 8: Machine Learning**
- Modelo de similaridade (cosine similarity)
- Embeddings de descrições técnicas
- Clustering de clientes por perfil

---

## 13. Considerações Finais

**Pipeline Completo:** De raw até refined, com validação rigorosa  
**Escalável:** Arquitetura medallion preparada para crescimento  
**Documentado:** Metadados completos no Datapedia  
**Seguro:** Criptografia AES-256 de dados sensíveis  
**Testado:** EDA com 50+ visualizações validadas  

**Próximas Etapas:**
1. Integração com Dadosfera
2. Dashboard Analytics
3. API de recomendação
4. Data App Streamlit

---

**Projeto:** Pipeline de Dados - Rolamentos Industriais  
**Atualizado:** 08/01/2026  
**Responsável:** Cryslayne Cinara

Gerado com Perplexity