# Modelagem de Dados

## 1. Objetivo da Modelagem

A modelagem de dados deste projeto tem como objetivo estruturar informações de **catálogo técnico de rolamentos**, **vendas** e **clientes** de forma analítica, permitindo:

* Análises descritivas de vendas e produtos
* Suporte à recomendação de produtos baseada em problemas técnicos
* Comparação de custo e oportunidade
* análise de histórico de vendas
* requisições em linguagem natural no data app

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


| Campo              | Tipo          | Descrição                                                  |
| ------------------ | ------------- | ---------------------------------------------------------- |
| product_id (PK)    | string        | Identificador único do produto                             |
| product_name       | string        | Nome comercial do produto                                  |
| category           | string        | Categoria principal do produto                             |
| bearing_type       | string        | Tipo de rolamento                                          |
| material           | string        | Material de fabricação                                     |
| load_capacity      | float         | Capacidade de carga suportada                              |
| max_speed          | float         | Velocidade máxima suportada                                |
| temperature_limit  | float         | Temperatura máxima de operação                             |
| technical_features | array<string> | Características técnicas extraídas ou enriquecidas via LLM |
| unit_cost          | float         | Custo unitário do produto                                  |
| list_price         | float         | Preço de tabela                                            |

**Objetivo:**

* Servir como base técnica para comparação de produtos e suporte às recomendações feitas pelo modelo de ML/LLM.

---

### 5.2 Dimensão Cliente – `dim_customer`

Representa os clientes industriais que compram os produtos.

| Campo                     | Tipo          | Descrição                                           |
| ------------------------- | ------------- | --------------------------------------------------- |
| customer_id (PK)          | string        | Identificador único do cliente                      |
| company_name              | string        | Nome da empresa                                     |
| industry                  | string        | Setor industrial de atuação                         |
| company_size              | string        | Porte da empresa (Pequena, Média, Grande)           |
| maintenance_model         | string        | Modelo de manutenção (Interna, Terceirizada, Mista) |
| equipment_criticality     | string        | Criticidade dos equipamentos                        |
| expected_problems         | array<string> | Problemas industriais esperados, derivados do setor |
| annual_revenue_estimated  | float         | Receita anual estimada                              |
| maintenance_budget_annual | float         | Orçamento anual de manutenção                       |
| downtime_cost_per_hour    | float         | Custo estimado de parada por hora                   |
| preferred_supplier        | boolean       | Indica se a empresa é cliente preferencial          |
| relationship_start_date   | date          | Início do relacionamento comercial                  |
| active                    | boolean       | Indica se o cliente está ativo                      |
| last_updated              | timestamp     | Última atualização do registro                      |


**Observação:**

O campo **expected_problems** foi incluído para resolver um gap conceitual identificado no projeto:
clientes industriais não compram produtos, mas soluções para problemas operacionais.

Esse atributo é derivado do setor (industry) e representa os problemas mais comuns enfrentados por empresas daquele segmento, como:

* Vibração
* Desgaste
* Superaquecimento
* Contaminação
* Corrosão

Esse campo é fundamental para:

* alinhar clientes e produtos por contexto técnico,
* permitir inferências no modelo de ML,
* conectar requisições em linguagem natural ao catálogo técnico.

---

### 5.3 Fato Vendas – `fact_sales`

Tabela central de eventos de venda.

| Campo                   | Tipo      | Descrição                       |
| ----------------------- | --------- | ------------------------------- |
| sale_id (PK)            | string    | Identificador único da venda    |
| sale_date               | date      | Data da venda                   |
| customer_id (FK)        | string    | Referência ao cliente           |
| product_id (FK)         | string    | Referência ao produto           |
| quantity                | int       | Quantidade vendida              |
| unit_price              | float     | Preço unitário praticado        |
| total_price             | float     | Valor total da venda            |
| discount_percentage     | float     | Percentual de desconto aplicado |
| sales_channel           | string    | Canal de venda                  |
| contract_type           | string    | Tipo de contrato                |
| payment_terms           | string    | Condições de pagamento          |
| delivery_lead_time_days | int       | Prazo de entrega                |
| sale_status             | string    | Status da venda                 |
| last_updated            | timestamp | Última atualização do registro  |

**Grão da tabela:**

> Uma linha por produto vendido por cliente em uma data.

Observação: pedidos com múltiplos produtos são representados por múltiplas linhas na tabela fato.

**Objetivo:**
Permitir análises históricas, validação de padrões de compra e apoio às recomendações técnicas.

---

## 6. Integração com Machine Learning e GenAI

As colunas technical_features são derivadas a partir dos campos textuais e categóricos do produto (technical_description, problem_types, applications), utilizando LLMs para normalização semântica, classificação técnica e enriquecimento de atributos.

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

* O campo expected_problems pode evoluir para uma tabela associativa (customer_problems) caso seja necessário maior granularidade.
* O modelo suporta enriquecimento adicional via LLM, sem necessidade de alteração estrutural.
* A modelagem prioriza clareza, coerência de domínio e aplicabilidade em um case técnico.

---

## 9. Conclusão

A modelagem proposta atende ao objetivo do projeto ao equilibrar:

* Simplicidade
* Escalabilidade
* Clareza analítica
* Integração com IA e Data Apps

Ela representa uma base sólida para demonstrar como a Dadosfera pode acelerar o caminho entre **dados técnicos complexos** e **valor de negócio**.

Gerado com ChatGPT
