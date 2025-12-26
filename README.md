# Projeto – Plataforma de Dados para Catálogo Técnico de Rolamentos

## Visão Geral

Este projeto é uma **Prova de Conceito (PoC)** de uma Plataforma de Dados construída para um cenário de **e-commerce industrial**, com foco em **catálogo técnico de rolamentos**, **vendas** e **suporte à decisão técnica e comercial**.

A solução demonstra como dados estruturados e desestruturados podem ser integrados, tratados, analisados e explorados utilizando a **plataforma Dadosfera**, com apoio de **Machine Learning** e **GenAI**, para acelerar o caminho entre **dados técnicos complexos** e **valor de negócio**.

O projeto foi desenvolvido como parte de um **case técnico**, seguindo as melhores práticas do ciclo de vida dos dados: integração, exploração, qualidade, processamento, análise, pipelines e entrega via Data App.

---

## Objetivo do Projeto

O principal objetivo é criar uma plataforma capaz de:

* Centralizar dados de catálogo técnico, vendas e clientes
* Transformar descrições técnicas em **features analíticas** utilizando LLMs
* Permitir que usuários descrevam **problemas industriais em linguagem natural**
* Recomendar produtos adequados com base em similaridade técnica
* Comparar **custo x oportunidade** para apoiar decisões de compra

---

## Escopo da Solução

### Dentro do escopo

* Catálogo técnico de rolamentos
* Histórico de vendas
* Perfil de clientes industriais
* Feature engineering com LLM
* Similaridade entre produtos
* Análises descritivas e temporais
* Data App interativo com Streamlit

### Fora do escopo

* Análises geográficas no Data App
* Processamento de dados em tempo real
* Integrações com sistemas externos de produção

---

## Arquitetura de Dados

A arquitetura segue o padrão recomendado pela Dadosfera, organizada em camadas:

* **Raw**: dados brutos no formato original
* **Trusted**: dados tratados e validados
* **Refined**: dados modelados para consumo analítico

A modelagem segue o padrão **Dimensional (Kimball)**, com tabelas fato e dimensões otimizadas para BI, ML e Data Apps.

Detalhes completos podem ser encontrados em:

* [`arquitetura.md`](docs/arquitetura.md)
* [`modelagem_dados.md`](docs/modelagem_dados.md)

---

## Estrutura do Repositório

```
📦 SEU_REPO
 ┣ 📂 data
 ┃ ┣ 📂 raw
 ┃ ┣ 📂 trusted
 ┃ ┗ 📂 refined
 ┣ 📂 notebooks
 ┃ ┣ 01_data_generation.ipynb
 ┃ ┣ 02_data_quality.ipynb
 ┃ ┣ 03_llm_feature_engineering.ipynb
 ┃ ┣ 04_eda_analysis.ipynb
 ┃ ┗ 05_ml_similarity.ipynb
 ┣ 📂 pipelines
 ┃ ┗ pipeline_etl.md
 ┣ 📂 data_app
 ┃ ┗ app.py
 ┣ 📂 docs
 ┃ ┣ arquitetura.md
 ┃ ┣ modelagem_dados.md
 ┃ ┗ planejamento.md
 ┗ README.md
```

---

## Dataset

Os dados utilizados representam um cenário realista de e-commerce industrial e foram **gerados sinteticamente** para fins educacionais.

Características:

* Mais de **100.000 registros**
* Dados estruturados (vendas, clientes)
* Dados semiestruturados e textuais (catálogo técnico)

Scripts e notebooks de geração estão disponíveis em:

* `01_data_generation.ipynb`

---

## Machine Learning e GenAI

O projeto utiliza técnicas de ML e GenAI para:

* Extração de features técnicas a partir de descrições textuais
* Criação de embeddings para produtos
* Cálculo de similaridade semântica
* Matching entre problemas descritos pelo usuário e produtos do catálogo

Essas etapas estão documentadas nos notebooks:

* `03_llm_feature_engineering.ipynb`
* `05_ml_similarity.ipynb`

---

## Data App

O Data App foi desenvolvido com **Streamlit** e tem como objetivo:

* Receber descrições de problemas técnicos em linguagem natural
* Analisar produtos disponíveis no catálogo
* Apresentar recomendações técnicas
* Comparar custo e oportunidade entre soluções

### Execução local

```bash
streamlit run data_app/app.py
```

Opcionalmente, o app pode ser publicado no **Streamlit Community Cloud**.

---

## Pipelines de Dados

O projeto inclui um pipeline de dados que contempla:

* ETL das camadas Raw → Trusted → Refined
* Validações de qualidade de dados
* Preparação de dados para ML

A documentação do pipeline está disponível em:

* `pipelines/pipeline_etl.md`

---

## Planejamento e Metodologia

O projeto foi planejado seguindo boas práticas de gestão, com foco em:

* Entregas incrementais
* Clareza de escopo
* Reprodutibilidade

O planejamento detalhado pode ser encontrado em:

* `docs/planejamento.md`

---

## Resultados Esperados

* Plataforma analítica funcional ponta a ponta
* Demonstração clara do ciclo de vida dos dados
* Aplicação prática de IA em dados industriais
* Base escalável para evoluções futuras

---

## Evoluções Futuras

* Inclusão de dados de manutenção e falhas
* Modelos preditivos de falha de rolamentos
* Integração com dados IoT
* Expansão do Data App para novos casos de uso

---

## Considerações Finais

Este projeto demonstra como a **Dadosfera** pode ser utilizada como uma solução completa para centralizar dados, aplicar inteligência artificial e entregar valor de forma ágil, mesmo em domínios técnicos complexos como o industrial.

Ele serve como uma prova de conceito de que é possível transformar dados técnicos em **insights acionáveis**, apoiando decisões estratégicas e operacionais.
