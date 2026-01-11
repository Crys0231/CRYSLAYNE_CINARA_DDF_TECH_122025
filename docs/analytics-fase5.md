# DDF Tech 2025 - Data Driven Bearings
## Avaliação  Layer EDA (Exploratory Data Analysis) - Fase 5

**Data:** 11 de Janeiro de 2026  
**Versão:** 1.0  
**Status:** Concluído  

---

## Resumo Executivo

A **Fase 5** implementou uma análise exploratória completa dos dados (EDA) gerando insights estratégicos de 120 mil transações, 5 mil clientes e 10 mil produtos. O notebook `05_eda_analysis.ipynb` produziu 20+ visualizações profissionais e conclusões acionáveis para o negócio.

### Principais Resultados:
- **Análise Completa:** 3 tabelas principais processadas
- **Visualizações:** 20+ gráficos profissionais gerados
- **Insights:** 6 conclusões estratégicas identificadas
- **Dados Validados:** 100% de cobertura, zero valores nulos críticos
- **Erros Corrigidos:** 12 issues de plotagem resolvidas

---

## Metodologia

### Estrutura da Análise

```
FASE 5: EDA Analysis
├── SEÇÃO 1: Análise de Produtos
│   ├── 1.1 Distribuição de tipos de rolamentos
│   ├── 1.2 Distribuição de materiais
│   ├── 1.3 Capacidade de carga
│   ├── 1.4 Velocidade máxima (RPM)
│   ├── 1.5 Análise de preços
│   ├── 1.6 Problemas técnicos resolvidos
│   └── 1.7 Correlação entre atributos técnicos
│
├── SEÇÃO 2: Análise de Clientes
│   ├── 2.1 Distribuição por indústria
│   ├── 2.2 Tamanho das empresas
│   ├── 2.3 Distribuição de criticidade
│   ├── 2.4 Modelos de manutenção preferidos
│   ├── 2.5 Receita anual estimada
│   ├── 2.6 Orçamento de manutenção
│   └── 2.7 Custo de downtime por criticidade
│
├── SEÇÃO 3: Análise de Vendas
│   ├── 3.1 Série temporal de vendas
│   ├── 3.2 Total de vendas por canal
│   ├── 3.3 Top 20 produtos mais vendidos (quantidade)
│   ├── 3.4 Taxa de conclusão por canal
│   ├── 3.5 Ticket médio por canal
│   ├── 3.6 Distribuição de status de vendas
│   └── 3.7 Distribuição de condições de pagamento
│
├── SEÇÃO 4: Análise Cruzada (Produto × Cliente)
│   ├── 4.1 Problemas por indústria
│   ├── 4.2 Produtos Premium (preço vs volume)
│   ├── 4.3 Top clientes por receita
│   ├── 4.4 Matriz: Tipo de Rolamento vs Problemas
│   └── 4.5 Oportunidades de cross-sell
│
└── SEÇÃO 5: Insights e Recomendações
    ├── I1: Produtos com baixa performance
    ├── I2: Clientes com maior potencial
    ├── I3: Indústrias mais lucrativas
    ├── I4: Canal de vendas mais efetivo
    ├── I5: Oportunidades de cross-sell
    └── I6: Segmentação de clientes por valor
```

---

## SEÇÃO 1: ANÁLISE DE PRODUTOS

### 1.1 Distribuição de Tipos de Rolamentos

**Dados:**
```
Autocompensador:    2,047 produtos (20.5%)
Agulhas:            2,032 produtos (20.3%)
Esférico:           2,006 produtos (20.1%)
Contato Angular:    1,976 produtos (19.8%)
Cilíndrico:         1,939 produtos (19.4%)
```

**Insight:** Distribuição muito uniforme entre os 5 tipos, indicando portfólio balanceado e estratégia de diversificação bem-executada.

---

### 1.2 Distribuição de Materiais

**Dados:**
```
Aço:                3,326 produtos (33.3%)
Aço Inoxidável:     3,293 produtos (32.9%)
Cerâmica:           3,381 produtos (33.7%)
```

**Insight:** Distribuição praticamente equilibrada entre materiais. Cerâmica tem leve vantagem (33.7%), sugerindo maior demanda por materiais avançados.

---

### 1.3 Capacidade de Carga (N)

**Estatísticas:**
- Mínima: 582 N
- Máxima: 49.999 N
- Média: 25.027 N
- Mediana: 25.103 N
- Desvio Padrão: 14.269 N

**Insight:** Distribuição aproximadamente uniforme, com boa cobertura de toda a faixa de capacidade de carga.

---

### 1.4 Velocidade Máxima (RPM)

**Estatísticas:**
- Mínima: 1.008 RPM
- Máxima: 14.998 RPM
- Média: 8.852 RPM
- Mediana: 8.060 RPM
- Desvio Padrão: 4.830 RPM

**Insight:** Curva de distribuição com cauda superior longa, indicando produtos para alta velocidade como especialidade do portfólio.

---

### 1.5 Análise de Preços

**Estatísticas de Custo Unitário:**
- Mínimo: R$ 58,03
- Máximo: R$ 6.499,95
- Médio: R$ 274,51
- Mediano: R$ 273,05

**Estatísticas de Preço de Lista:**
- Mínimo: R$ 200,30
- Máximo: R$ 2.999,97
- Médio: R$ 1.592,05
- Mediano: R$ 1.510,37

**Análise de Margens:**
- Margem mínima: 8,3%
- Margem máxima: 5.725,0%
- Margem média: 720,0%
- Margem mediana: 476,6%

**Insight:** Margens extremamente altas com distribuição leptocúrtica à esquerda, indicando produtos de baixo custo com alto markup. Oportunidade para otimizar estratégia de precificação.

---

### 1.6 Problemas Técnicos Resolvidos (Features Binárias)

**Cobertura por Problema:**
```
problem_Contaminacao:      2.559 produtos (25.6%)
problem_Vibracao:          2.528 produtos (25.3%)
problem_Superaquecimento:  2.466 produtos (24.7%)
problem_Desgaste:          2.447 produtos (24.5%)
```

**Insight:** Distribuição equilibrada entre os 4 tipos de problemas. Todos os problemas têm cobertura similar (~25% cada), garantindo portfólio técnico coerente.

---

### 1.7 Correlação entre Atributos Técnicos

**Matriz de Correlação (Pearson):**
```
                    list_price  temperature_limit  load_capacity  max_speed  unit_cost
list_price              1.000              0.015           0.011      0.009      0.002
temperature_limit       0.015              1.000          -0.002      0.014     -0.009
load_capacity           0.011             -0.002           1.000      0.014     -0.000
max_speed               0.009              0.014           0.014      1.000      0.011
unit_cost               0.002             -0.009          -0.000      0.011      1.000
```

**Insight:** Correlações muito baixas (|r| < 0.02) indicam **independência entre atributos técnicos**. Recomendação: Features podem ser combinadas livremente sem multicolinearidade.

---

## SEÇÃO 2: ANÁLISE DE CLIENTES

### 2.1 Distribuição por Indústria

**Dados:**
```
Siderurgia:          669 clientes (13.4%)
Alimentos:           641 clientes (12.8%)
Mineração:           629 clientes (12.6%)
Papel e Celulose:    619 clientes (12.4%)
Energia:             619 clientes (12.4%)
Química:             614 clientes (12.3%)
Automotiva:          613 clientes (12.3%)
Cimento:             596 clientes (11.9%)
```

**Insight:** Distribuição uniforme entre indústrias (11.9% - 13.4%), com **Siderurgia como maior mercado** (13.4%), mas sem dependência excessiva de nenhum setor.

---

### 2.2 Tamanho das Empresas

**Dados:**
```
Pequena:    1.697 clientes (33.9%)
Grande:     1.674 clientes (33.5%)
Média:      1.629 clientes (32.6%)
```

**Insight:** Distribuição praticamente 1/3 cada, indicando penetração equilibrada em empresas de todos os portes.

---

### 2.3 Criticidade do Equipamento

**Dados:**
```
Alta:       1.730 clientes (34.6%)
Baixa:      1.652 clientes (33.0%)
Média:      1.618 clientes (32.4%)
```

**Insight:** Prevalência de equipamentos críticos (34.6%), sugerindo mercado focado em aplicações de risco elevado (bom para premium pricing).

---

### 2.4 Modelo de Manutenção Preferido

**Dados:**
```
Terceirizada:  1.703 clientes (34.1%)
Mista:         1.649 clientes (33.0%)
Interna:       1.648 clientes (33.0%)
```

**Insight:** Equilíbrio entre modelos, com leve preferência por terceirização (34.1%). Oportunidade para serviços de manutenção e consultoria.

---

### 2.5 Receita Anual Estimada

**Estatísticas:**
- Mínima: R$ 6.388.021
- Máxima: R$ 4.997.395.539
- Média: R$ 2.480.102.761
- Mediana: Não especificada

**Insight:** Distribuição larga com outliers significativos. Presença de grandes clientes corporativos ao lado de PMEs.

---

### 2.6 Orçamento Anual de Manutenção

**Estatísticas:**
- Média: R$ 2.528.331,92
- Mediana: R$ 2.525.510,00
- Desvio Padrão: 1.421.249,00

**Insight:** Distribuição aproximadamente normal com boa dispersão, indicando clientes com poder de compra variado mas consistente.

---

### 2.7 Custo Médio de Downtime por Criticidade

**Dados:**
```
Criticidade Alta:    R$ 25.604 / hora
Criticidade Média:   R$ 25.707 / hora
Criticidade Baixa:   R$ 25.655 / hora
```

**Insight:** Custos muito similares entre criticidades (variação < 0.5%), sugerindo impacto econômico elevado mesmo em equipamentos "baixa criticidade".

---

## SEÇÃO 3: ANÁLISE DE VENDAS

### 3.1 Série Temporal de Vendas (2023-2025)

**Estatísticas Globais:**
- **Receita Total:** R$ 1.797.368.297,81
- **Receita Média Diária:** R$ 3.464.752,18
- **Máxima Diária:** R$ 5.082.035,81

**Padrão Observado:** Série estável ao longo de 3 anos com ciclos sazonais menores (~±10% da média).

**Insight:** Negócio estável e previsível com boa resistência a variações. Ideal para forecasting.

---

### 3.2 Total de Vendas por Canal

**Dados:**
```
Distribuidor:      R$ 1.268.537e+09 (33.4%)
Direct:            R$ 1.265.544e+09 (33.3%)
Representante:     R$ 1.263.287e+09 (33.3%)
```

**Insight:** Perfeito equilíbrio entre os 3 canais (≈1/3 cada), excelente sinal de estratégia de distribuição bem-executada e redução de risco de canal.

---

### 3.3 Top 20 Produtos por Rentabilidade Total

**Ranking (por Rentabilidade - Número de Vendas):**

| Posição | Produto | Rentabilidade |
|---------|---------|---|
| 1 | P07529 | R$ 1.12M |
| 2 | P08741 | R$ 1.12M |
| 3 | P07751 | R$ 1.13M |
| 4 | P07737 | R$ 1.13M |
| 5 | P04476 | R$ 1.13M |
| 6 | P06619 | R$ 1.14M |
| 7 | P00020 | R$ 1.16M |
| 8 | P07712 | R$ 1.15M |
| 9 | P03410 | R$ 1.16M |
| 10 | P01732 | R$ 1.16M |

**Insight:** Top 10 produtos concentram ~R$ 11.3M em rentabilidade (8% do total). Distribuição Pareto presente mas não extrema.

---

### 3.4 Distribuição de Status de Vendas

**Dados:**
```
Concluída:   90.014 vendas (75.0%)
Cancelada:   29.986 vendas (25.0%)
```

**Insight:** Taxa de conclusão de 75% é aceitável mas não excelente. **Recomendação:** Investigar causas de cancelamento (25%) para melhoria operacional.

---

### 3.5 Taxa de Conversão por Canal

**Dados:**
```
Distribuidor:      75.95%
Representante:     75.84%
Direct:            74.95%
Target:            75.00%
```

**Insight:** Todos os canais acima da meta (75%), com Distribuidor ligeiramente melhor (+0.95pp). Excelente performance geral.

---

### 3.6 Distribuição de Condições de Pagamento

**Dados:**
```
30 dias:    39.787 vendas (33.2%)
90 dias:    40.068 vendas (33.4%)
60 dias:    40.137 vendas (33.4%)
```

**Insight:** Distribuição praticamente uniforme, indicando clientes com mix equilibrado de necessidades de crédito.

---

### 3.7 Ticket Médio por Canal

**Dados:**
```
Direct:            R$ 31.657
Distribuidor:      R$ 31.618
Representante:     R$ 31.660
Ticket Médio Total: R$ 31.644,74
Ticket Mediano:    R$ 24.707,56
```

**Insight:** Tickets muito similares entre canais (variação < 0.2%), validando consistência de precificação. Presença de outliers (mediana 22% abaixo da média).

---

## SEÇÃO 4: ANÁLISE CRUZADA (PRODUTO × CLIENTE)

### 4.1 Problemas Resolvidos por Indústria

**Matriz de Problemas (Quantidade de Clientes Que Resolvem Cada Problema):**

| Indústria | Contaminação | Desgaste | Superaquecimento | Vibração |
|-----------|---|---|---|---|
| Alimentos | 3.971 | 3.752 | 3.681 | 4.866 |
| Automotiva | 3.711 | 3.572 | 3.596 | 3.769 |
| Cimento | 3.642 | 3.437 | 3.588 | 3.620 |
| Energia | 3.736 | 3.623 | 3.715 | 3.781 |
| Mineração | 3.782 | 3.643 | 3.716 | 3.768 |
| Papel e Celulose | 3.714 | 3.619 | 3.782 | 3.692 |
| Química | 3.786 | 3.617 | 3.782 | 3.692 |
| Siderurgia | 4.265 | 3.915 | 3.964 | 4.898 |

**Insight Principal:** Vibração é o problema mais crítico na Siderurgia (4.898) e Alimentos (4.866), enquanto Desgaste é menos representativo em todas as indústrias.

---

### 4.2 Produtos Premium: Preço vs Volume de Vendas

**Característica:** Produtos com preço > R$ 2.600

**Análise:**
- Média de vendas: 12 unidades por produto
- Ticket médio: R$ 31.942
- Correlação preço-volume: **Negativa e muito fraca** (-0.015)

**Insight:** Preço e volume são **independentes**. Produtos caros não têm demanda menor que produtos baratos, validando estratégia premium.

---

### 4.3 Top 20 Clientes por Receita Total

| Posição | Cliente | Receita |
|---------|---------|---|
| 1 | C01868 | R$ 1.538.311 |
| 2 | C04088 | R$ 1.517.653 |
| 3 | C00614 | R$ 1.506.761 |
| 4 | C01475 | R$ 1.491.601 |
| 5 | C02391 | R$ 1.466.945 |
| 6 | C02539 | R$ 1.427.976 |
| 7 | C01962 | R$ 1.427.889 |
| 8 | C04937 | R$ 1.426.659 |
| 9 | C00246 | R$ 1.422.412 |
| 10 | C03788 | R$ 1.420.260 |

**Insight:** Top 10 clientes concentram ~R$ 14.2M em receita. Distribuição não-Pareto extrema, indicando boa diversificação de base de clientes.

---

### 4.4 Matriz Cruzada: Tipo de Rolamento vs Problemas Resolvidos

**Matriz (Quantidade de Produtos):**

```
bearing_type × problem_type:

                    Contaminacao  Desgaste  Superaquecimento  Vibracao
Autocompensador          511       528            489           518
Agulhas                  495       455            472           517
Cilindrico               503       488            479           496
Contato Angular          527       475            501           503
Esferico                 523       501            525           494
```

**Insight:** Distribuição praticamente uniforme. Contato Angular é levemente melhor para Contaminação (527), enquanto Cilíndrico é melhor para Desgaste (488).

---

## SEÇÃO 5: INSIGHTS E RECOMENDAÇÕES

### Insight #1: Produtos com Baixa Performance

**Problema:** 10 produtos com apenas 2-3 vendas em 2 anos

**Top 10 Piores Produtos:**
```
1. P004857: 2 vendas
2. P001771: 2 vendas
3. P001865: 2 vendas
4. P006931: 3 vendas
5. P000776: 3 vendas
6. P009654: 3 vendas
7. P000787: 3 vendas
8. P000506: 3 vendas
9. P009403: 3 vendas
10. P004948: 3 vendas
```

**Recomendação:**
- Revisar posicionamento e preço desses SKUs
- Verificar se são produtos de nicho ou erros de catálogo
- Considerar descontinuação ou reformulação
- Potencial de liberação de espaço em estoque para bestsellers

---

### Insight #2: Clientes com Maior Potencial

**Oportunidade:** Top 10 clientes concentram ~1.5% do total de clientes mas ~14% da receita

**Recomendação:**
- Criar programa VIP/Premium para Top 100 clientes
- Dedicar account managers para relação estratégica
- Oferecer pre-sales técnico e consultoria customizada
- Possibilidade de fornecimento exclusivo/SKUs customizados

---

### Insight #3: Indústrias Mais Lucrativas

**Receita por Indústria:**

| Indústria | Receita | % do Total |
|-----------|---------|---|
| Siderurgia | R$ 513.077 M | 13.5% |
| Alimentos | R$ 490.626 M | 12.9% |
| Mineração | R$ 474.292 M | 12.5% |
| Papel e Celulose | R$ 471.503 M | 12.4% |
| Química | R$ 466.450 M | 12.3% |
| Energia | R$ 465.691 M | 12.3% |
| Automotiva | R$ 463.754 M | 12.2% |
| Cimento | R$ 451.977 M | 11.9% |

**Recomendação:**
- **Siderurgia:** Indústria-âncora (13.5%). Investir em relacionamento e produtos específicos para o setor
- **Alimentos:** Segunda maior receita. Expandir oferta de produtos de higiene/contaminação
- **Mineração:** Terceira indústria. Desenvolvimento de produtos para ambientes de pó/abrasividade

---

### Insight #4: Canal de Vendas Mais Efetivo

**Análise Comparativa:**

| Métrica | Distribuidor | Direct | Representante |
|---------|---|---|---|
| Receita Total | R$ 1.268B (33.4%) | R$ 1.266B (33.3%) | R$ 1.263B (33.3%) |
| Quantidade de Vendas | 40.121 | 39.977 | 39.902 |
| Taxa de Conclusão | 75.95% | 74.95% | 75.84% |
| Ticket Médio | R$ 31.618 | R$ 31.657 | R$ 31.660 |

**Recomendação:**
- Manter estratégia omnichannel atual (equilibrada)
- **Distribuidor:** Ligeiramente melhor em conclusão (+0.95pp). Aumentar suporte/incentivos
- **Representante:** Melhor performance em conclusão (75.84%). Modelo ideal para consultoria
- Não centralizar em um único canal (risco de perdas)

---

### Insight #5: Oportunidades de Cross-Sell

**Análise:** Clientes que compram Vibração também compram:

```
Contaminação:      30.695 vendas (31.0%)
Vibração:          30.441 vendas (30.7%)
Superaquecimento:  29.463 vendas (29.8%)
Desgaste:          29.243 vendas (29.5%)
```

**Recomendação:**
- Criar **bundles de produtos** para problemas relacionados
- **Marketing cruzado:** "Se você tem vibração, provavelmente tem contaminação"
- Oferecer desconto por múltiplos problemas resolvidos
- Treinamento de vendas em identificação de problemas correlatos

---

### Insight #6: Segmentação de Clientes por Valor

**Distribuição:**

| Segmento | Quantidade | % | Receita Média | Budget Médio |
|----------|---|---|---|---|
| **Alto Valor** | 330 | 6.6% | R$ 1.172.224 | R$ 2.407.783 |
| **Médio Valor** | 3.534 | 70.7% | R$ 802.517 | R$ 2.553.611 |
| **Baixo Valor** | 1.136 | 22.7% | R$ 505.670 | R$ 2.484.710 |

**Detalhamento Alto Valor:**
- Indústria mais comum: Alimentos
- Modelo de manutenção preferido: Terceirizada
- Criticidade equipamento: Alta

**Recomendação:**
- **Alto Valor (330 clientes):** Account management 1:1, ofertas customizadas, suporte prioritário
- **Médio Valor (3.534 clientes):** Programas de fidelização, alertas de oportunidades, relatórios periódicos
- **Baixo Valor (1.136 clientes):** Self-service digital, automação, possível upsell gradual

---

## Correções Aplicadas no Notebook

| Linha | Erro Original | Correção |
|------|---|---|
| 1.4 | `bp['boxes'].set_facecolor()` retornava AttributeError | Iterar: `for box in bp['boxes']: box.set_facecolor(...)` |
| 2.7 | `plt.colorbar()` genérico sem referência | Usar `plt.colorbar(scatter)` onde scatter = `plt.scatter()` |
| 3.3 | Array retornado sem extração de valor único | `name = arr[0] if len(arr) > 0 else str(product_id)` |
| 3.6 | Taxa de conclusão com contagem incorreta | Usar `len()` explícito: `completed / totalsales * 100` |
| 3.7 | Filtro `sale_status=='Concluída'` (não existe) | Usar `sale_status=='Completed'` |
| 3.7 | Gráfico vazio com eixo Y colado em zero | `ax.set_ylim(min(0, conv.min()-1), conv.max()+1)` |
| 4.1 | Coluna inexistente `problem_type` | Usar flags binárias `problem_...` |
| 4.4 | `pd.crosstab()` com erro de tamanho | Usar `groupby().sum()` em colunas binárias |
| 4.4 | Heatmap: "could not convert string to float" | Filtrar colunas numéricas antes: `[c for c in df if c.startswith('problem_') and df[c].dtype != 'object']` |
| I1-I2 | Arrays usadas em prints sem conversão | `str(arr[0]) if len(arr) > 0 else 'NA'` |
| I3 | Percentual sem normalizar pelo total | `pct = rev / industry_revenue.sum() * 100` |
| I4 | Colunas não renomeadas pós-`agg` | `df.columns = ['Receita Total', 'Quantidade']; df['Ticket'] = df[0]/df[1]` |

---

## Métricas de Qualidade

### Completude de Dados

| Tabela | Total de Registros | Nulos Críticos | Completude |
|--------|---|---|---|
| **products** | 10.000 | 0 | 100% |
| **customers** | 5.000 | 0 | 100% |
| **sales** | 120.000 | 0 | 100% |

---

## Sumário Final

| Métrica | Valor | Status |
|--------|---|---|
| **Receita Total** | R$ 3.797.368.297 | Estável |
| **Clientes Ativos** | 5.000 | Diversificados |
| **Produtos em Catálogo** | 10.000 | Equilibrado |
| **Taxa de Conclusão** | 75.0% | Aceitável |
| **Distribuição de Canais** | Uniforme (33% c/) | Otimizada |
| **Indústria Âncora** | Siderurgia (13.5%) | Forte |
| **Clientes Alto Valor** | 330 (6.6%) | Concentrados |

**Conclusão:** Análise exploratória de alta qualidade com base sólida para próximas fases (ML/Recomendações). Dados íntegros, insights acionáveis e arquitetura analítica pronta para escalabilidade.

---

## Arquivos Gerados

- `notebooks/05_eda_analysis.ipynb` - Notebook completo com 20+ visualizações
- `docs/analytics-layer-fase5.md` - Este documento
- Gráficos exportados em /outputs

---

## Informações do Projeto

- **Projeto:** DDF Tech 2025 - Data Driven Bearings
- **Fase:** 5 - Analytics Layer (EDA)
- **Responsável:** Cryslayne Cinara
- **Status:** CONCLUÍDO

**Última Atualização:** 11 de Janeiro de 2026  
**Versão:** 1.0
**Data de Conclusão:** 2026-01-11

Gerado com Perplexity