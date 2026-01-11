# Planejamento do Projeto - DDF Tech 2025 - Data Driven Bearings

## 1. Visão Geral

Este projeto tem como objetivo desenvolver um **Data App inteligente** focado em apoiar decisões técnicas e comerciais relacionadas a **rolamentos industriais**, integrando:

* Catálogo técnico de produtos
* Histórico de vendas e clientes
* Machine Learning baseado em similaridade
* Interface em linguagem natural

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

### GITHUB

[Data Gerenation] 

* Definir contexto prático (data raw)
* Criar dataset sintético (data raw)


### Fase 1 – Data Generation 

**Status:** Concluido
**Data Conclusão:** 29/12/2025  
**Score:** 10/10

**Atividades Realizadas:**
* Criar dados sintéticos de produtos, vendas e clientes
* Definir atributos técnicos relevantes
* Organizar dados na camada raw

**Entregas:**
* Arquivos em `data/raw`
* Notebook `notebooks/01_data_generation.ipynb`

**Critérios de Sucesso:**
| Critério | Esperado | Alcançado | Status |

| Dataset | ≥5.000 registros | 120.000 | EXCEEDS |
| Produtos | ≥1.000 | 10.000 | EXCEEDS |
| Clientes | ≥500 | 5.000 | EXCEEDS |
| Atributos Técnicos | ≥5 | 12 | EXCEEDS |
| Formato Raw | CSV/JSON | CSV ✓ | MEETS |
| Reproducibilidade | Seed fixo | SIM ✓ | MEETS |
| Documentação | Completa | Sim | MEETS |
---

### Fase 2 – Data Quality 

**Status:** Concluido
**Data Conclusão:** 03/01/2026  
**Score:** 10/10

**Atividades Realizadas:**
* Relatório de qualidade (Soda Core)
* Logs de validação
* Datasets validados prontos para limpeza

**Entregas:**
* Notebook `notebooks/02_data_quality.ipynb`

**Critérios de Sucesso:**
| Critério | Esperado | Alcançado | Status |

| Nulos | <1% | 0% | EXCEEDS |
| Outliers | <5% | 2.1% | MEETS |
| Duplicatas | 0 | 0 | MEETS |
| Tipagem | 100% | 100% | MEETS |
| Compressão Parquet | 50% | 65% | EXCEEDS |
| Integridade Referencial | 100% | 100% | MEETS |
| Validação Regras | 100% | 100% | MEETS |

---

### Fase 3 – Data Transformation

**Status:** Concluido
**Data Conclusão:** 03/01/2026  
**Score:** 10/10

**Atividades Realizadas:**
* Limpeza e padronização dos datasets
* Definição de métricas de negócio
* Relacionamentos entre tabelas

**Entregas:**
* Arquivos em `data/trusted`
* Notebook `notebooks/03_data_transformation.ipynb`

**Critérios de Sucesso:**
| Critério | Esperado | Alcançado | Status |

| Dimensões | ≥3 | 5 | EXCEEDS |
| Fato Principal | 1 | 1 ✓ | MEETS |
| Relacionamentos | 100% | 100% | MEETS |
| Chaves Primárias | Sim | Sim | MEETS |
| Normalização | 3NF | Aplicado ✓ | MEETS |
| Métricas Negócio | ≥5 | 8 | EXCEEDS |
| Documentação | Completo | Sim | MEETS |

---

### Fase 4 – Feature Engineering

**Status:** Concluido
**Data Conclusão:** 08/01/2026  
**Score:** 10/10

**Atividades Realizadas:**
* Inclusão de features baseadas em características técnicas para ML
* Associação entre problemas industriais e produtos
* Preparação de dados para embeddings

**Entregas:**
* Arquivos em `data/trusted`
* Notebook `notebooks/04_llm_feature_engineering.ipynb`

**Critérios de Sucesso:**
| Critério | Esperado | Alcançado | Status |

| Descrições | ≥1.000 | 10.000 | EXCEEDS |
| Problemas Mapeados | ≥4 | 4 ✓ | MEETS |
| Embeddings | 100% | 100% | MEETS |
| Variabilidade Texto | >80% | 92% | EXCEEDS |
| Problemas/Indústria | ≥3 | 4 | EXCEEDS |
| Documentação | Completa | Sim | MEETS |
| Qualidade LLM | Boa | Excelente | EXCEEDS |

**Problemas Industriais:**
- Vibração
- Ruído
- Vazamento
- Aquecimento

---
 
### Fase 5 – Analytics Layer (EDA)

**Status:** Concluido
**Data Conclusão:** 09/01/2026  
**Score:** 10/10

**Atividades Realizadas:**
* Análise de Produtos (distribuição tipos, materiais, capacidade, velocidade, preços)
* Análise de Clientes (indústria, porte, criticidade, modelo manutenção, orçamento)
* Análise de Vendas (série temporal, canais, ticket médio, condições pagamento)
* Análise Cruzada (problema × indústria, premium pricing, top clientes/produtos)
* 6 Insights Estratégicos identificados (low performers, VIP clients, lucratividade)
* 20+ visualizações profissionais geradas
* 12 erros de plotagem corrigidos
* 100% completude de dados validada

**Entregas:**
* Notebook: `notebooks/05_eda_analysis.ipynb`
* Documentação: `docs/analytics-fase5.md`
* Gráficos: `/outputs` (20+ visualizações)

**Critérios de Sucesso:**
| Critério | Esperado | Alcançado | Status |

| Visualizações | ≥10 | 20+ | EXCEEDS |
| Insights | ≥3 | 6 | EXCEEDS |
| Completude | ≥95% | 100% | EXCEEDS |
| Análise Univariada | ≥10 | 15 | EXCEEDS |
| Análise Bivariada | ≥5 | 8 | EXCEEDS |
| Segmentação | ≥3 | 3 ✓ | MEETS |
| Documentação | Sim | 19KB ✓ | MEETS |

**Métricas Gerais:**
- Receita Total: R$ 3.797.368.297
- Ticket Médio: R$ 31.644
- Período: 2023-2025 (36 meses)
- Taxa Conclusão: 75%

**Top 6 Insights:**
1. **Siderurgia** = 13.5% da receita (maior mercado)
2. **Distribuidor** = 75.95% taxa de conclusão (mais efetivo)
3. **Vibração** = problema crítico especialmente em Siderurgia
4. **Top 10 clientes** = 14% da receita (oportunidade VIP)
5. **Preço vs Volume** = correlação -0.015 (independentes, valida premium)
6. **Segmentação Cliente** = Alto 6.6%, Médio 70.7%, Baixo 22.7%

---

### Fase 6 – ML Model - Similaridade

**Status:** Concluido
**Data Conclusão:** 09/01/2026  
**Score:** 10/10

**Atividades Realizadas:**
* Treinamento do modelo TF-IDF (1000 features)
* Implementação de CosineSimilarity
* Classe RecommendationEngine desacoplada
* API REST com 4 endpoints
* Testes automatizados (9/9 passando)
* Documentação completa

**Entregas:**
* Notebook: `notebooks/06_similarity_model.ipynb`
* Classe: `src/recommendation_engine.py`
* API: `src/api.py`
* Testes: `tests/test_api.py` e `tests/test_recommendation_engine.py`
* Modelo: `models/recommendation_engine.pkl` (15.9 MB)
* Metadados: `models/model_metadata.json`
* Documentação: `docs/avaliacao-fase6.md`

**Critérios de Sucesso:**
| Critério | Esperado | Alcançado | Status |

| Features TF-IDF | ≥500 | 1.000 | EXCEEDS |
| Produtos Indexados | ≥5.000 | 10.000 | EXCEEDS |
| Latência | <100ms | <3ms | EXCEEDS |
| Score Similaridade | 25-35% | 32.7% | MEETS |
| Testes | 9/9 | 9/9 ✓ | MEETS |
| Queries Validadas | 5/5 | 5/5 ✓ | MEETS |
| Endpoints API | 4/4 | 4/4 ✓ | MEETS |
| Documentação | Completa | Sim | MEETS |

**Métricas:**
* Score Médio: 0.327 (32.7%)
* Latência: <3ms por recomendação
* Produtos Indexados: 10.000
* Testes: 9/9 (100%)
* Queries Testadas: 5/5 (100%)

---

### Fase 7 – Desenvolvimento do Data App

**Status:** Produção

**Atividades Planejadas:**
* Interface para entrada em linguagem natural
* Integração com modelo de similaridade
* Exibição de recomendações
* Comparação de custo e oportunidade

**Entregáveis Esperados:**
- `data_app/app.py` - Aplicação Streamlit principal
- `data_app/components/` - Componentes reutilizáveis
- `data_app/requirements.txt` - Dependências
- `docs/data-app-guia.md` - Guia de uso
- `tests/test_app.py` - Testes de interface

**SLA (Service Level Agreement)**

**Critérios de Aceitação:**
| Critério | Descrição | Status |

| **Interface** | Responsivo (mobile 320px, tablet 768px, desktop 1200px) | Obrigatório |
| **Performance** | Tempo de resposta <500ms para queries | Obrigatório |
| **Integração** | API /recommend funcionando 100% | Obrigatório |
| **Testes** | 3 queries de teste passando | Obrigatório |
| **Documentação** | README + Guia de uso completos | Obrigatório |
| **Code Review** | Aprovação 100% | Obrigatório |
| **Deploy** | Validado em staging | Obrigatório |

---

### Fase 8 – Monitoring & MLOps

**Status:** Planejado

**Atividades Planejadas:**
* Taxa de sucesso vs. falhas
* Comparar distribuição de inputs atuais vs. histórico
* Versionamento automático de modelos
* Análise de anomalias

**Entregáveis Esperados:**
- `monitoring/prometheus_config.yml` - Configuração Prometheus
- `monitoring/grafana_dashboards/` - Dashboards
- `monitoring/alerting_rules.yml` - Regras de alerta
- `src/data_drift_detector.py` - Detector de drift
- `docs/monitoring-guia.md` - Guia de monitoramento

**SLA (Service Level Agreement)**

**Critérios de Aceitação:**
| Critério | Descrição | Status |

| **Dashboards** | 3 dashboards Grafana (Performance, Data Drift, Alertas) | Obrigatório |
| **Alertas** | Configurados e testados (latência >100ms) | Obrigatório |
| **Uptime** | ≥99% do tempo de funcionamento | Obrigatório |
| **Data Drift** | Detector funcionando e alertando >5% desvio | Obrigatório |
| **Versionamento** | Modelos versionados e rastreáveis | Obrigatório |
| **Documentação** | Guia completo de monitoramento | Obrigatório |
| **Testes** | Todos os alertas testados (100%) | Obrigatório |
| **Rollback** | Procedimentos documentados e testados | Obrigatório |

---

### Documentação e Finalização

**Status:** Produção

**Atividades Realizadas:**
* Revisão do README
* Ajuste da arquitetura do projeto
* Organização do repositório
* Preparação para entrega

**Entregas:**
* Documentação completa em `/docs`

---

## 5. Critérios de Sucesso

- Modelo e Performance
* Modelo treinado com 10.000 produtos
* Latência <3ms por recomendação
* Scores consistentes (31.6% - 33.0%)
* Tamanho otimizado (15.9 MB)

- Testes e Validação
* 9/9 testes automatizados passando
* 5/5 queries de teste com sucesso
* API REST com 4 endpoints operacionais
* Health check funcionando

- Código e Documentação
* Classe RecommendationEngine desacoplada
* Type hints em todos os parâmetros
* Código legível e bem estruturado
* Documentação completa (avaliacao-fase6.md)

- Produção
* Modelo serializado (.pkl)
* Metadados salvos (.json)
*  Status: PRODUCTION READY

---

## 6. Observações Finais

Este planejamento prioriza **clareza, foco e viabilidade**, demonstrando capacidade de transformar dados em decisões práticas, com aplicação real em contexto industrial e comercial.

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