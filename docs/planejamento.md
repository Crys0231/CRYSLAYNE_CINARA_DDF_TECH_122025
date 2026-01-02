# Planejamento do Projeto

## 1. Visão Geral

Este projeto tem como objetivo desenvolver um **Data App inteligente** focado em apoiar decisões técnicas e comerciais relacionadas a **rolamentos industriais**, integrando:

* Catálogo técnico de produtos
* Histórico de vendas e clientes
* Machine Learning baseado em similaridade
* Interface em linguagem natural

O escopo foi intencionalmente **enxugado** para garantir foco, qualidade e entrega dentro do prazo, removendo funcionalidades secundárias como análise geográfica no app.

---

## 2. Objetivo do Projeto

Construir uma solução capaz de:

* Permitir que usuários descrevam **problemas industriais em linguagem natural**
* Analisar o catálogo técnico para identificar produtos adequados
* Comparar **custo atual vs custo de oportunidade**
* Apoiar decisões de substituição ou melhoria de componentes

---

## 3. Escopo do Projeto

### 3.1 Dentro do Escopo

* Pipeline de dados (raw → trusted → refined)
* Modelagem analítica (dimensões e fatos)
* Feature engineering com descrições técnicas
* Modelo de similaridade semântica
* Data App com input em linguagem natural
* Recomendações de produtos
* Comparação de custo e oportunidade

---

## 4. Fases do Projeto

### Fase 1 – Preparação e Geração de Dados

**Status:** Base do projeto

Atividades:

* Criar dados sintéticos de produtos, vendas e clientes
* Definir atributos técnicos relevantes
* Organizar dados na camada raw

Entrega:

* Arquivos em `/data/raw`
* Notebook `01_data_generation.ipynb`

### GITHUB

[Data Gerenation] 

* Definir contexto prático (data raw)
* Criar dataset sintético (data raw)

---

### Fase 2 – Qualidade e Camada Trusted

Atividades:

* Limpeza de dados
* Padronização de tipos
* Tratamento de nulos e inconsistências
* Conversão para formato parquet

Entrega:

* Arquivos em `/data/trusted`
* Notebook `02_data_quality.ipynb`

---

### Fase 3 – Modelagem Analítica (Refined)

Atividades:

* Criação das dimensões e fato
* Definição de métricas de negócio
* Relacionamentos entre tabelas

Entrega:

* Arquivos em `/data/refined`
* Documento `modelagem_dados.md`

---

### Fase 4 – Feature Engineering com LLM

Atividades:

* Criação de descrições técnicas textuais
* Associação entre problemas industriais e produtos
* Preparação de dados para embeddings

Entrega:

* Notebook `03_llm_feature_engineering.ipynb`

---

### Fase 5 – Análise Exploratória (EDA)

Atividades:

* Análise de vendas por tipo de produto
* Identificação de padrões de falha e substituição
* Insights de custo vs oportunidade

Entrega:

* Notebook `04_eda_analysis.ipynb`

---

### Fase 6 – Modelo de Similaridade

Atividades:

* Geração de embeddings de texto
* Implementação de similaridade vetorial
* Ranking de produtos recomendados

Entrega:

* Notebook `05_ml_similarity.ipynb`

---

### Fase 7 – Desenvolvimento do Data App

Atividades:

* Interface para entrada em linguagem natural
* Integração com modelo de similaridade
* Exibição de recomendações
* Comparação de custo e oportunidade

Entrega:

* Arquivo `/data_app/app.py`

---

### Fase 8 – Documentação e Finalização

Atividades:

* Revisão do README
* Ajuste da arquitetura do projeto
* Organização do repositório
* Preparação para entrega

Entrega:

* Documentação completa em `/docs`

---

## 5. Critérios de Sucesso

* Pipeline funcional e organizado
* Recomendações coerentes a partir de linguagem natural
* Comparação clara de custo e oportunidade
* Código legível e bem documentado
* Escopo bem definido e executado

---

## 6. Observações Finais

Este planejamento prioriza **clareza, foco e viabilidade**, demonstrando capacidade de transformar dados em decisões práticas, com aplicação real em contexto industrial e comercial.

Gerado com ChatGPT