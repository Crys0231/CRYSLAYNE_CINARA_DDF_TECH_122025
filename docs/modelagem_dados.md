# Modelagem de Dados

## 1. Objetivo da Modelagem

A modelagem de dados deste projeto tem como objetivo estruturar informações de **catálogo técnico de rolamentos**, **vendas** e **clientes** de forma analítica, permitindo:

* Análises descritivas de vendas e produtos
* Suporte à recomendação de produtos baseada em problemas técnicos
* Comparação de custo e oportunidade
* Escalabilidade para uso de Machine Learning e GenAI

A modelagem foi pensada para um **cenário de e-commerce industrial**, alinhada às boas práticas de Data Warehousing e à arquitetura da plataforma Dadosfera.

---

## 2. Abordagem de Modelagem Escolhida

Foi adotada a **modelagem dimensional (Kimball)**, pois:

* Facilita análises analíticas e exploração via SQL e BI
* É amplamente utilizada em cenários de vendas e produtos
* Integra-se bem com dashboards, Data Apps e pipelines de ML
* É adequada para ambientes orientados a consumo de dados

O modelo segue o padrão **Star Schema**, com uma tabela fato central e dimensões bem definidas.

---

## 3. Visão Geral do Modelo

O modelo final é composto por:

* **1 Tabela Fato**

  * `fact_sales`

* **2 Tabelas Dimensão**

  * `dim_product`
  * `dim_customer`

Essas tabelas estão localizadas na camada **Refined**, prontas para consumo analítico.

---

## 4. Camadas do Data Lake

A organização dos dados segue o padrão recomendado pela Dadosfera:

### 4.1 Raw

Dados brutos, sem tratamento:

* `products_raw.json`
* `sales_raw.csv`
* `customers_raw.csv`

Características:

* Dados no formato original
* Sem validação ou padronização
* Fonte única da verdade

---

### 4.2 Trusted

Dados tratados e confiáveis:

* `products_trusted.parquet`
* `sales_trusted.parquet`
* `customers_trusted.parquet`

Transformações aplicadas:

* Padronização de tipos de dados
* Tratamento de valores nulos
* Normalização de campos textuais
* Enriquecimento inicial de dados

---

### 4.3 Refined

Dados modelados para análise:

* `dim_product.parquet`
* `dim_customer.parquet`
* `fact_sales.parquet`

Camada otimizada para:

* BI
* Machine Learning
* Data Apps

---

## 5. Descrição das Tabelas

### 5.1 Dimensão Produto – `dim_product`

Contém informações técnicas e comerciais dos rolamentos.

**Principais campos:**

* `product_id` (PK)
* `product_name`
* `category`
* `bearing_type`
* `material`
* `load_capacity`
* `max_speed`
* `temperature_limit`
* `technical_features` (features extraídas via LLM)
* `unit_cost`
* `list_price`

**Observações:**

* As colunas técnicas são utilizadas tanto para análise quanto para similaridade semântica
* Features textuais são processadas por LLM na etapa de feature engineering

---

### 5.2 Dimensão Cliente – `dim_customer`

Representa os clientes industriais que compram os produtos.

**Principais campos:**

* `customer_id` (PK)
* `customer_name`
* `industry_segment`
* `company_size`
* `purchase_profile`
* `created_at`

**Observações:**

* Dados de localização podem existir, mas não são utilizados no Data App
* Permite análises de perfil de compra e recorrência

---

### 5.3 Fato Vendas – `fact_sales`

Tabela central de eventos de venda.

**Principais campos:**

* `sale_id` (PK)
* `product_id` (FK)
* `customer_id` (FK)
* `sale_date`
* `quantity`
* `unit_price`
* `total_amount`
* `discount`

**Grão da tabela:**

> Uma linha por produto vendido por cliente em uma data.

---

## 6. Integração com Machine Learning e GenAI

A modelagem foi pensada para suportar os seguintes casos:

* Similaridade entre produtos baseada em características técnicas
* Matching entre problema descrito em linguagem natural e produtos do catálogo
* Análises de custo vs oportunidade

As features extraídas via LLM são armazenadas na dimensão de produto, permitindo:

* Reuso das features
* Redução de custo computacional
* Consistência entre análises

---

## 7. Visões Analíticas Derivadas

A partir do modelo, são possíveis pelo menos duas visões analíticas principais:

### 7.1 Visão Comercial

* Vendas por categoria de produto
* Evolução temporal de faturamento
* Produtos mais vendidos
* Clientes com maior volume de compra

### 7.2 Visão Técnica / Oportunidade

* Produtos recomendados por tipo de problema
* Comparação de custo entre soluções
* Identificação de oportunidades de upsell

---

## 8. Evoluções Futuras

Este modelo permite evoluções como:

* Inclusão de novas dimensões (tempo, fornecedor, manutenção)
* Ampliação para Data Vault
* Integração com dados de sensores (IoT)
* Análises preditivas de falha

---

## 9. Conclusão

A modelagem proposta atende ao objetivo do projeto ao equilibrar:

* Simplicidade
* Escalabilidade
* Clareza analítica
* Integração com IA e Data Apps

Ela representa uma base sólida para demonstrar como a Dadosfera pode acelerar o caminho entre **dados técnicos complexos** e **valor de negócio**.
