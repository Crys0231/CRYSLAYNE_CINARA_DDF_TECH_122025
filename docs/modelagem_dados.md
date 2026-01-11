# Modelagem de Dados - DDF Tech 2025 - Data Driven Bearings

**Data:** 11/01/2026 
**Status Geral:** **FASES 1-6 PRODUCTION READY**  
**Responsável:** Cryslayne Cinara   
**Versão:** 2.0

---
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

| Campo                   | Tipo          | Descrição                                                 | Criptografado (Dadosfera) |
|-------------------------|---------------|-----------------------------------------------------------|---------------------------|
| product_id (PK)         | string        | Identificador único do produto                            | NÃO                       |
| product_name            | string        | Nome comercial do produto                                 | NÃO                       |
| product_category        | string        | Categoria principal (ex: Rolamentos, Mancais)             | NÃO                       |
| product_subcategory     | string        | Subcategoria (ex: Esférico, Cilíndrico)                   | NÃO                       |
| manufacturer            | string        | Fabricante (ex: SKF, NSK, FAG, Timken, NTN)               | NÃO                       |
| model                   | string        | Modelo do fabricante (ex: MD-859)                         | NÃO                       |
| bearing_type            | string        | Tipo de rolamento técnico                                 | NÃO                       |
| material                | string        | Material de fabricação                                    | NÃO                       |
| load_capacity           | float         | Capacidade de carga suportada (Newtons)                   | NÃO                       |
| max_speed               | int           | Velocidade máxima suportada (RPM)                         | NÃO                       |
| temperature_limit       | int           | Temperatura máxima de operação (°C)                       | NÃO                       |
| problem_type            | string        | Tipo de problema principal que resolve                    | NÃO                       |
| unit_cost               | float         | Custo unitário do produto (R$)                            | SIM                       |
| list_price              | float         | Preço de tabela (R$)                                      | SIM                       |
| technical_description   | string        | Descrição técnica completa gerada (camada Trusted)        | -                         |
| technical_features      | array<string> | Tags categóricas extraídas (Features)                     | -                         |
| supported_problems      | array<string> | Problemas que o produto pode resolver (Features)          | -                         |
| llm_product_description | string        | Descrição enriquecida para embeddings (Features)          | -                         |

**Objetivo:**

* Servir como base técnica para comparação de produtos e suporte às recomendações feitas pelo modelo de ML/LLM.
  
**supported_problems** Matching entre query do cliente e produtos recomendados. Este campo é fundamental para o modelo TF-IDF, pois contém os problemas que cada produto resolve (vibração, desgaste, superaquecimento, contaminação). Permite que recomendações sejam baseadas em contexto técnico.

**llm_product_description** Base para vetorização TF-IDF. Combinada com supportedproblems, fornece o vocabulário completo para cálculo de similaridade coseno entre query do cliente e produtos.

---

### 5.2 Dimensão Cliente – `dim_customer`

Representa os clientes industriais que compram os produtos.

| Campo                     | Tipo          | Descrição                                           | Criptografado (Dadosfera) |
|---------------------------|---------------|-----------------------------------------------------|---------------------------|
| customer_id (PK)          | string        | Identificador único do cliente                      | NÃO                       |
| company_name              | string        | Nome da empresa                                     | SIM                       |
| industry                  | string        | Setor industrial de atuação                         | NÃO                       |
| company_size              | string        | Porte da empresa (Pequena, Média, Grande)           | NÃO                       |
| maintenance_model         | string        | Modelo de manutenção (Interna, Terceirizada, Mista) | NÃO                       |
| equipment_criticality     | string        | Criticidade dos equipamentos (Baixa, Média, Alta)   | NÃO                       |
| expected_problems         | array<string> | Problemas esperados por setor industrial (Features) | -                         |
| annual_revenue_estimated  | float         | Receita anual estimada (R$)                         | SIM                       |
| maintenance_budget_annual | float         | Orçamento anual de manutenção (R$)                  | SIM                       |
| downtime_cost_per_hour    | float         | Custo estimado de parada por hora (R$)              | SIM                       |
| preferred_supplier        | boolean       | Indica se é cliente preferencial                    | NÃO                       |
| relationship_start_date   | date          | Início do relacionamento comercial                  | NÃO                       |
| active                    | boolean       | Indica se o cliente está ativo                      | NÃO                       |
| last_updated              | timestamp     | Última atualização do registro                      | NÃO                       |

**Observação:**

O campo **expected_problems** foi incluído (gerado no arquivo 03, tratado no 04) para resolver um gap conceitual identificado no projeto:
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

| Campo                   | Tipo      | Descrição                                | Criptografado (Dadosfera) |
|-------------------------|-----------|------------------------------------------|---------------------------|
| sale_id (PK)            | string    | Identificador único da venda             | NÃO                       |
| sale_date               | date      | Data da venda                            | NÃO                       |
| customer_id (FK)        | string    | Referência ao cliente (dim_customer)     | SIM                       |
| product_id (FK)         | string    | Referência ao produto (dim_product)      | NÃO                       |
| quantity                | int       | Quantidade vendida                       | NÃO                       |
| unit_price              | float     | Preço unitário praticado (R$)            | SIM                       |
| total_price             | float     | Valor total da venda (R$)                | SIM                       |
| discount_percentage     | int       | Percentual de desconto aplicado          | SIM                       |
| sales_channel           | string    | Canal de venda                           | NÃO                       |
| contract_type           | string    | Tipo de contrato                         | NÃO                       |
| payment_terms           | string    | Condições de pagamento                   | NÃO                       |
| delivery_lead_time_days | int       | Prazo de entrega em dias                 | NÃO                       |
| sale_status             | string    | Status da venda                          | NÃO                       |
| last_updated            | timestamp | Última atualização do registro           | NÃO                       |

**Grão da tabela:**

> Uma linha por produto vendido por cliente em uma data.

Observação: pedidos com múltiplos produtos são representados por múltiplas linhas na tabela fato.

**Objetivo:**
Permitir análises históricas, validação de padrões de compra e apoio às recomendações técnicas.

---

## 6. Integração com Machine Learning e GenAI

**Fases 1-5 - Feature Engineering com LLM + EDA**

A coluna technical_features é derivada a partir dos campos textuais e categóricos do produto (technical_description, problem_types), utilizando LLMs para normalização semântica, classificação técnica e enriquecimento de atributos.

**Fase 5 - EDA Analysis**

Análise exploratória completa gerou insights críticos para o modelo:
**Produtos:** Distribuição uniforme (20% cada tipo), independência entre atributos técnicos (|r| < 0.02)
**Clientes:** 8 indústrias equilibradas, Siderurgia líder (13.4%), 3 modelos manutenção
**Vendas:** 3 canais com receita idêntica (~33% cada), 75% conclusão
**Problemas:** Vibração crítica (Siderurgia 4.898), Contaminação equilibrada (25.6% produtos)
**Correlações:** Preço/Volume = -0.015 (independentes), validando premium pricing

**Fase 6 - Modelo de Similaridade TF-IDF**

Integração com modelo implementado em `src/recommendation_engine.py`:
**Input:** Combinação de technical_description + supported_problems
**Processamento:** TfidfVectorizer (1000 features) + CosineSimilarity
**Output:** Top-K produtos com scores 31.6%-33.0%
**Performance:** <3ms por recomendação
**Acurácia:** 9/9 automatizados (100%), 5/5 queries de teste

A modelagem foi pensada para suportar os seguintes casos:
**Suporte multi-canal** (Direct, Distributor, Representative)
**Segmentação de clientes** (Alto/Médio/Baixo Valor)
**Similaridade entre produtos** baseada em características técnicas
**Matching entre problema** descrito em linguagem natural e produtos do catálogo
**Análises de custo vs oportunidade** para decisões comerciais
**Recomendações automáticas** via API REST com latência baixa

---

## 7. Visões Analíticas Derivadas

### 7.1 Visão Comercial (Análise de Vendas)
- Vendas por categoria de produto
- Evolução temporal de faturamento
- Produtos mais vendidos
- Clientes com maior volume de compra

**Resultados Fase 5:**
- Receita total: R$ 3.797.368.297
- Ticket médio: R$ 31.644
- Canais equilibrados: 33% cada (Direct, Distributor, Representative)
- Série temporal: Estável 2023-2025 com ±10% variação
- Top 20 produtos: 8% do faturamento

### 7.2 Visão Técnica - Oportunidade
- Produtos recomendados por tipo de problema
- Comparação de custo entre soluções
- Identificação de oportunidades de upsell

**Resultados Fase 5:**
- 4 problemas técnicos mapeados (25% cobertura cada)
- Vibração: crítica em Siderurgia (4.898 vendas)
- Margem média: 720% (produto de baixo custo + alto markup)
- 10 produtos com baixa performance (2-3 vendas em 2 anos)
- Cross-sell: Vibração → Contaminação (30.7% dos clientes)

### 7.3 Visão de Recomendação - Fase 6
Baseada no modelo TF-IDF implementado, esta visão permite:

| Capacidade | Descrição | Entrada | Saída |

| **Recomendação por Problema** | Identifica produtos que resolvem problema | Query em linguagem natural | Top-K com scores |
| **Ranking de Relevância** | Ordena por similaridade técnica | Descrição do problema | Scores 31.6%-33.0% |
| **Suporte Multi-Idioma** | Português, inglês, espanhol | Qualquer idioma | Recomendações consistentes |
| **Batch Processing** | Múltiplas queries | Array de queries | Array de recomendações |
| **API Metadata** | Info sobre modelo | GET /api/v1/metadata | JSON com TF-IDF params |

**Tecnologia:**
- Modelo: scikit-learn (TfidfVectorizer + CosineSimilarity)
- Produtos: 10.000 indexados
- Features: 1.000 termos únicos
- Latência: <3ms por recomendação
- Testes: 9/9 automatizados (100%)

**Casos de Uso:**
1. Cliente: "Máquina vibrando muito"
2. API recomenda: [Rolamento 9412 (0.328), Rolamento 5637 (0.327), ...]
3. Data App: Cards com produtos, especificações, preços
4. Usuário: Comparar custo vs benefício, fazer pedido

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

---

## Informações do Projeto

- **Projeto:** DDF Tech 2025 - Data Driven Bearings
- **Escopo:** 8 Fases planejadas, 6 concluídas
- **Status:** **FASES 1-6 PRODUCTION READY**
- **Responsável:** Cryslayne Cinara
- **Data de Atualização:** 11 de Janeiro de 2026
- **Versão:** 2.0

---

**Gerado com ChatGPT, Perplexity e análise estratégica de projeto**
