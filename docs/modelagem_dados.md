# DDF Tech 2025 - Data Driven Bearings
## Estrutura de dados

**Data:** 28/01/2026 
**Status Geral:** **COMPLETED**  
**Responsável:** Cryslayne Cinara   
**Versão:** 2.0

---

## Resumo

A modelagem de dados segue a metodologia **Kimball** com **Star Schema** implementado em 3 tabelas (1 fato + 2 dimensões), estruturando catálogo técnico de rolamentos (10.000), clientes (5.000) e 120 mil transações de vendas. A modelagem segue o padrão **Medallion** e integra análise descritiva, recomendação baseada em problemas técnicos e suporte a machine learning com embeddings TF-IDF.

---

## 1. Objetivo da Modelagem

A modelagem estrutura informações para:

- **Análises descritivas:** Vendas, produtos, clientes
- **Recomendações técnicas:** Mapeamento problema → solução
- **Comparação comercial:** Custo atual vs oportunidade
- **Histórico:** Padrões de compra e preferências
- **ML Natural Language:** Queries em linguagem natural

---

## 2. Abordagem Escolhida

### 2.1 Padrão: Modelagem Dimensional (Kimball)

**Motivos:**
- Facilita análises analíticas e exploração SQL
- Amplamente adotado em vendas e produtos
- Integra bem com dashboards, Data Apps e ML
- Orientado ao consumo de dados

### 2.2 Estrutura: Star Schema

```
         ┌─────────────────┐
         │  dim_customer   │
         │  (5.000 filas)  │
         │  ┌───────────┐  │
         │  │customer_id│  │
         │  │company... │  │
         │  │industry   │  │
         │  └───────────┘  │
         └────────┬────────┘
                  │
         ┌────────┴────────┐
         │                 │
    ┌────▼────────────────▼─────┐
    │   fact_sales              │
    │  (120.000 linhas)         │
    │  ┌──────────────────────┐ │
    │  │sale_id (PK)          │ │
    │  │customer_id (FK)      │ │
    │  │product_id (FK)       │ │
    │  │quantity, price, ...  │ │
    │  └──────────────────────┘ │
    └────┬──────────────────────┘
         │
         └────────┬─────────────┐
                  │             │
         ┌────────▼────────┐    │
         │  dim_product    │    │
         │(10.000 filas)   │    │
         │  ┌──────────┐   │    │
         │  │product_id│   │    │
         │  │name      │   │    │
         │  │technical │   │    │
         │  │features  │   │    │
         │  └──────────┘   │    │
         └─────────────────┘    │
                                │
                    (RelaçõesFK)
```

---

## 3. Camadas do Data Lake

### 3.1 Raw Zone (Ingestão) - `01_data_generation.ipynb`

**Dados brutos, sem tratamento**

| Arquivo | Registros | Campos | Características |
| ------- | --------- | ------ | --------------- |
| `products_raw.json` | 10.000 | 14 | JSON, sem validação |
| `customers_raw.csv` | 5.000 | 13 | CSV, sem normalização |
| `sales_raw.csv` | 120.000 | 14 | CSV, sem limpeza |

**Função:** Source of truth original

### 3.2 Trusted Zone (Validação) - `03_data_transformation.ipynb`

**Dados tratados e confiáveis**

| Arquivo | Registros | Transformações |
| ------- | --------- | -------------- |
| `products_trusted.parquet` | 10.000 | Tipo, margens, descrição técnica |
| `customers_trusted.parquet` | 5.000 | Tipo, mapeamento indústria |
| `sales_trusted.parquet` | 120.000 | Data normalizada, validações |

**Transformações Aplicadas:**
- 359 campos com margem negativa - Regra de negócio normalizada (set list_price = unit_cost * 1.25 (margem mínima 25%))
- Padronização de tipos de dados
- Tratamento de valores nulos
- Normalização de campos textuais
- Enriquecimento inicial (descrições técnicas, problemas)
- Validação de conformidade (99.7%)

**Conformidade:** 99.7% (359 erros corrigidos)

### 3.3 Refined Zone (Modelagem) - `04_feature_engineering.ipynb`

**Dados modelados para análise**

| Tabela | Registros | Tipo | Função |
| ------ | --------- | ---- | ------ |
| `dim_product` | 10.000 | Dimensão  | Características técnicas e comerciais |
| `dim_customer` | 5.000 | Dimensão  | Contexto industrial e operacional |
| `fact_sales` | 120.000 | Fato  | Eventos de vendas |

**Otimizações:**
- Star Schema implementado
- Índices de chave primária
- Chaves estrangeiras validadas
- Pronto para BI, ML, Data Apps

---

## 4. Tabela de Dimensão: Produtos

### 4.1 Estrutura: `dim_product`

**Contém:** Informações técnicas e comerciais dos rolamentos

**Volume:** 10.000 registros

| Campo | Tipo | Descrição | Cripto |
| ----- | ---- | --------- | ------ |
| **product_id** (PK) | string | Identificador único | NÃO |
| **product_name** | string | Nome comercial | NÃO |
| **product_category** | string | Categoria principal | NÃO |
| **product_subcategory** | string | Subcategoria | NÃO |
| **manufacturer** | string | Fabricante (SKF, NSK, FAG, etc) | NÃO |
| **model** | string | Modelo do fabricante | NÃO |
| **bearing_type** | string | Tipo técnico | NÃO |
| **material** | string | Material fabricação | NÃO |
| **load_capacity** | float | Capacidade carga (N) | NÃO |
| **max_speed** | int | Velocidade máxima (RPM) | NÃO |
| **temperature_limit** | int | Temperatura máxima (°C) | NÃO |
| **problem_type** | string | Problema principal resolvido | NÃO |
| **unit_cost** | float | Custo unitário (R$) | SIM |
| **list_price** | float | Preço de tabela (R$) | SIM |
| **technical_description** | string | Descrição técnica (gerada) | NÃO |
| **technical_features** | array | Tags categóricas extraídas | NÃO |
| **supported_problems** | array | Problemas resolvidos | NÃO |
| **llm_product_description** | string | Descrição enriquecida (embeddings) | NÃO |

### 4.2 Exemplos de Dados

```json
{
  "product_id": "P09412",
  "product_name": "Rolamento Esférico SKF 6409",
  "bearing_type": "Esférico",
  "supported_problems": ["vibração", "desgaste"],
  "technical_features": ["alta_velocidade", "baixa_fricção"],
  "load_capacity": 12500.0,
  "max_speed": 8500,
  "unit_cost": 45.50,
  "list_price": 99.99,
  "llm_product_description": "Rolamento esférico de contato angular..."
}
```

---

## 5. Tabela de Dimensão: Clientes

### 5.1 Estrutura: `dim_customer`

**Contém:** Contexto industrial e operacional dos clientes

**Volume:** 5.000 registros

| Campo | Tipo | Descrição | Cripto |
| ----- | ---- | --------- | ------ |
| **customer_id** (PK) | string | Identificador único | NÃO |
| **company_name** | string | Nome da empresa | SIM |
| **industry** | string | Setor industrial | NÃO |
| **company_size** | string | Porte (Pequena/Média/Grande) | NÃO |
| **maintenance_model** | string | Modelo manutenção | NÃO |
| **equipment_criticality** | string | Criticidade (Baixa/Média/Alta) | NÃO |
| **expected_problems** | array | Problemas esperados por setor | NÃO |
| **annual_revenue_estimated** | float | Receita anual (R$) | SIM |
| **maintenance_budget_annual** | float | Orçamento manutenção (R$) | SIM |
| **downtime_cost_per_hour** | float | Custo parada/hora (R$) | SIM |
| **preferred_supplier** | boolean | Cliente preferencial | NÃO |
| **relationship_start_date** | date | Início relacionamento | NÃO |
| **active** | boolean | Cliente ativo | NÃO |
| **last_updated** | timestamp | Última atualização | NÃO |

### 5.2 Valor do Campo: `expected_problems`

**Novo campo estratégico** que mapeia problemas esperados por indústria:

| Indústria | Problemas Esperados |
| --------- | ------------------- |
| Siderurgia | Vibração, Desgaste, Corrosão |
| Alimentos | Contaminação, Corrosão, Higiêne |
| Mineração | Desgaste, Contaminação, Vibração |
| Automóvel | Vibração, Ruído, Temperatura |

**Função:**
- Alinhar contexto do cliente com produtos
- Inferências no modelo de ML
- Matching entre query e catálogo

---

## 6. Tabela de Fato: Vendas

### 6.1 Estrutura: `fact_sales`

**Contém:** Eventos de venda e transações

**Volume:** 120.000 registros

**Grão:** Uma linha por produto vendido por cliente em uma data
*(Pedidos com múltiplos produtos = múltiplas linhas)*

| Campo | Tipo | Descrição | Cripto |
| ----- | ---- | --------- | ------ |
| **sale_id** (PK) | string | Identificador único | NÃO |
| **sale_date** | date | Data da venda | NÃO |
| **customer_id** (FK) | string | Referência cliente | SIM |
| **product_id** (FK) | string | Referência produto | NÃO |
| **quantity** | int | Quantidade vendida | NÃO |
| **unit_price** | float | Preço unitário (R$) | SIM |
| **total_price** | float | Valor total (R$) | SIM |
| **discount_percentage** | int | Percentual desconto | SIM |
| **sales_channel** | string | Canal (Direct, Distributor, Rep) | NÃO |
| **contract_type** | string | Tipo de contrato | NÃO |
| **payment_terms** | string | Condições pagamento | NÃO |
| **delivery_lead_time_days** | int | Prazo entrega (dias) | NÃO |
| **sale_status** | string | Status venda | NÃO |
| **last_updated** | timestamp | Última atualização | NÃO |

### 6.2 Distribuição: Sales

```
Período: Jan 2023 - Dez 2025 (36 meses)
Receita: R$ 3.797.368.297
Ticket Médio: R$ 31.644

Canais (equilibrados):
├─ Direct: 33% (~1.266M transações)
├─ Distributor: 33% (~1.266M transações)
└─ Representative: 33% (~1.266M transações)

Status:
├─ Concluída: 75% (90K transações)
└─ Pendente: 25% (30K transações)
```

---

## 7. Integrações com Machine Learning

### 7.1 Fase 4: Feature Engineering com LLM

**Enriquecimento de dados para ML:**

| Campo | Origem | Uso |
| ----- | ------ | --- |
| technical_description | LLM + manual | Fonte para TF-IDF |
| technical_features | LLM extraction | Features categóricas |
| supported_problems | LLM generation | Matching queries |
| expected_problems | Mapeamento indústria | Contexto cliente |
| llm_product_description | LLM embedding | Vetorização |

### 7.2 Fase 6: Modelo TF-IDF

**Entrada:** `technical_description` + `supported_problems`

**Processamento:**
```
TfidfVectorizer(max_features=1000)
↓
CosineSimilarity(query_vector, produto_vectors)
↓
Top-K com scores (0.316 - 0.330)
```

**Output:** Recomendações em <3ms

### 7.3 Fase 5: Análise Exploratória

**Insights gerados:**

| Insight | Descoberta | Ação |
| ------- | ---------- | ---- |
| **I1 - Low Performers** | 10 produtos com 2-3 vendas | Descontinuar |
| **I2 - VIP Clients** | Top 10 = 14% receita | Programa VIP |
| **I3 - Market Anchors** | Siderurgia 13.5% | Foco Marketing |
| **I4 - Omnichannel** | Canais equilibrados | Manter estratégia |
| **I5 - Cross-sell** | Vibração→Contaminação 31% | Bundling |
| **I6 - Segmentação** | VIP 6.6%, Médio 70.7% | Estratégias customizadas |

--- 

## 8. Camada de Logging e Monitoramento

### 8.1 Estrutura de Histórico de Consultas

#### Tabela: query_history
```json
{
  "query": "string (problema técnico)",
  "timestamp": "datetime (quando consultado)",
  "count": "int (número de resultados)",
  "top_score": "float (score do melhor resultado)",
  "processing_time_ms": "float (latência em ms)",
  "user_id": "string (identificação do usuário)",
  "drift_detected": "boolean (se drift foi detectado)",
  "alerts": "array (alertas disparados)"
}

// Estrutura: Métricas do Monitoramento
{
  "timestamp": "datetime",
  "metric_type": "string (cpu, memory, latency, drift)",
  "value": "float",
  "threshold": "float",
  "alert_level": "string (info, warning, critical)",
  "status": "string (healthy, degraded, critical)"
}
```

### 6.2 Sistema de Alertas

| Alerta            | Condição              | Severidade | Ação                     |
| ----------------- | --------------------- | ---------- | ------------------------ |
| High CPU          | CPU > 80%             | WARNING    | Log + Dashboard          |
| Critical Memory   | Memory > 85%          | CRITICAL   | Log + Notify + Dashboard |
| Data Drift        | Score std > threshold | WARNING    | Log + Dashboard          |
| Model Performance | Latência > 100ms      | WARNING    | Log + Dashboard          |
| System Down       | API não responde      | CRITICAL   | Alert + Dashboard        |

### 6.3 Versionamento de Modelos

models/
├── recommendation_engine_v1.pkl (2026-01-10, baseline)
└── metadata.json
  └── version: "1.0"
  └── training_date: "2026-01-10"
  └── n_features: 1000
  └── n_products: 10000
  └── vocab_size: 1000

---

## 8. Visões Analíticas Derivadas

### 8.1 Visão Comercial

**Análise de vendas:**
- Vendas por categoria
- Evolução temporal
- Produtos mais vendidos
- Top clientes

**Resultados:**
- Receita: R$ 3.797.368.297
- Ticket: R$ 31.644
- Canais: 33% cada
- Top 20 produtos: 8% faturamento

### 8.2 Visão Técnica

**Oportunidade e soluções:**
- Produtos recomendados × problema
- Comparação custo
- Identificação upsell

**Resultados:**
- 4 problemas mapeados (25% cobertura)
- Vibração crítica em Siderurgia
- Margem média: 720%
- 10 produtos baixa performance

### 8.3 Visão de Recomendação

**ML baseado em similaridade:**

| Capacidade | Input | Output |
| ---------- | ----- | ------ |
| Recomendação | Query natural | Top-K com scores |
| Ranking | Problema descrito | Produtos ordenados |
| Multi-idioma | Português/Inglês/Espanhol | Consistente |
| Batch | Array de queries | Array de recos |

**Performance:**
- Latência: <3ms
- Produtos: 10.000 indexados
- Features: 1.000
- Testes: 100%

---

## 9. Conclusão

A modelagem proposta atende ao objetivo do projeto ao equilibrar:

* Simplicidade
* Escalabilidade
* Clareza analítica
* Integração com IA e Data Apps

Ela representa uma base sólida para demonstrar como a Dadosfera pode acelerar o caminho entre **dados técnicos complexos** e **valor de negócio**.

## 9. Validações de Integridade

### 9.1 Chaves Primárias

| Tabela | Campo | Validação | Status |
| ------ | ----- | --------- | ------ |
| `dim_product` | product_id | Unicidade | 100% |
| `dim_customer` | customer_id | Unicidade | 100% |
| `fact_sales` | sale_id | Unicidade | 100% |

### 9.2 Chaves Estrangeiras

| FK | Referência | Conformidade | Status |
| -- | ---------- | ------------ | ------ |
| `fact_sales.customer_id` → `dim_customer` | 5.000 únicos | 100% |
| `fact_sales.product_id` → `dim_product` | 10.000 únicos | 100% |

### 9.3 Regras de Negócio

| Regra | Validação | Resultado |
| ----- | --------- | --------- |
| Margens | list_price > unit_cost | 99.7% (359 corrigidas) |
| Preços | total_price = quantity × unit_price | 100% |
| Descontos | 0 ≤ discount ≤ 100 | 100% |
| Datas | sale_date ≤ hoje | 100% |

---

## 10. Segurança de Dados

### 10.1 Criptografia (Dadosfera AES-256)

| Campo | Motivo |
| ----- | ------ |
| company_name | PII - Nome empresa |
| unit_cost | Financeiro |
| list_price | Financeiro |
| annual_revenue_estimated | Financeiro |
| maintenance_budget_annual | Financeiro |
| unit_price | Financeiro |
| total_price | Financeiro |
| downtime_cost_per_hour | Financeiro |

### 10.2 Conformidade

- LGPD (Lei Geral de Proteção de Dados)
- Criptografia AES-256
- Acesso auditado
- Retenção controlada

---

## 11. Escalabilidade

### 11.1 Capacidade Atual vs Futura

| Aspecto | Atual | Futuro | 
| ------- | ----- | ------ | 
| Produtos | 10.000 | 100.000+ |
| Clientes | 5.000 | 50.000+ | 
| Transações | 120.000 | 1.000.000+ |
| Storage | 95 MB | <1 GB | 
| Latência queries | <1s | <5s | 

### 11.2 Estratégias

- Particionamento por ano (fact_sales)
- Índices em FK e datas
- Compressão Parquet (65%)
- Cachê de dimensões

---

## 12. Documentação de Referência

### Arquivos Relacionados

| Documento | Foco | Referência |
| --------- | ---- | ---------- |
| `arquitetura.md` | Camadas e tecnologia | Medallion pattern |
| `planejamento.md` | Roadmap e fases | Fase 4: Feature eng |
| `analytics-fase5.md` | Análises e insights | EDA detalhada |
| `avaliacao-fase6.md` | Modelo ML | TF-IDF performance |
| `data_app-fase7.md` | Escopo da aplicação | Aplicação Streamit |
| `monitoring-fase8.md` | Sistema de monitoramento | 5+ camadas de monitoramento |

---

## 13. Conclusão

A modelagem dimensional do **Data Driven Bearings** equilibra:

- **Simplicidade:** 3 tabelas com relacionamentos claros
- **Escalabilidade:** Suporta 100K+ produtos
- **Clareza analítica:** Star Schema bem definido
- **Integração ML:** Features prontas para TF-IDF
- **Conformidade:** 99.7% qualidade de dados

A estrutura é **sólida, viável e extensível** para evolução futura.

---

## Informações do Projeto

- **Projeto:** DDF Tech 2025 - Data Driven Bearings
- **Escopo:** 8 Fases completas
- **Status:** **READY**
- **Responsável:** Cryslayne Cinara
- **Data de Atualização:** 28 de Janeiro de 2026
- **Versão:** 2.0

**IAs Utilizadas no Projeto:**

- **Perplexity PRO** - Pesquisa aprofundada e levantamento de referências
- **Claude** - Validação de documentação e revisão estrutural
- **ChatGPT** - Geração de escopo inicial e planejamento
- **Manus.ai** - Construção e refinamento do código-fonte

**Nota:** As decisões finais, análises críticas e direcionamentos estratégicos foram conduzidos pela autora do projeto, com a IA atuando como ferramenta de apoio.