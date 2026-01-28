"""
Página Sobre - Redesenhada com Storytelling
"""

import streamlit as st
from data_app.utils.session import setup_paths, get_engine, get_data
from data_app.utils.history import ensure_history_exists
from data_app.components.layout import (
    get_global_css,
    render_sidebar,
    render_footer
)

# Setup paths uma única vez
setup_paths()

# Garantir histórico
ensure_history_exists()

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(
    page_title="Sobre o Projeto",
    page_icon="ℹ️",
    layout="wide"
)

# Garantir engine está inicializado
if 'engine' not in st.session_state:
    with st.spinner("⚙️ Inicializando sistema..."):
        engine = get_engine()
        if engine is None:
            st.error("❌ Não foi possível inicializar o sistema. Tente recarregar a página.")
            st.stop()
        st.session_state.engine = engine

# Garantir dados estão carregados
if 'products_data' not in st.session_state:
    st.session_state.products_data = get_data()

# SIDEBAR
render_sidebar()

# APLICAR ESTILO GLOBAL PADRONIZADO
st.markdown(get_global_css(), unsafe_allow_html=True)

# ============================================================================
# CSS ESPECÍFICO DA PÁGINA
# ============================================================================

st.markdown("""
<style>
    /* Problem/Solution Cards */
    .problem-solution-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 32px;
        height: 100%;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .problem-card {
        border-left: 4px solid var(--error);
    }
    
    .solution-card {
        border-left: 4px solid var(--success);
    }
    
    .problem-solution-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 102, 204, 0.2);
    }
    
    /* Stats Grid */
    .stat-box {
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 180, 216, 0.05) 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 102, 204, 0.4);
    }
    
    .stat-number {
        font-size: 36px;
        font-weight: 700;
        color: var(--secondary);
        margin-bottom: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    .stat-label {
        font-size: 14px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Timeline */
    .timeline-item {
        position: relative;
        padding-left: 40px;
        padding-bottom: 24px;
        border-left: 2px solid rgba(0, 102, 204, 0.3);
    }
    
    .timeline-item:last-child {
        border-left: 2px dashed rgba(0, 102, 204, 0.3);
    }
    
    .timeline-dot {
        position: absolute;
        left: -9px;
        top: 0;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: var(--success);
        border: 3px solid #0F172A;
    }
    
    .timeline-dot.pending {
        background: var(--warning);
    }
    
    /* Tech Badge */
    .tech-badge {
        display: inline-block;
        background: rgba(0, 102, 204, 0.1);
        border: 1px solid rgba(0, 102, 204, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        font-size: 12px;
        font-weight: 600;
        color: var(--secondary);
        font-family: 'Inter', sans-serif;
    }
    
    .cta-section {
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.15) 0%, rgba(0, 180, 216, 0.15) 100%);
        border: 2px solid var(--border-color);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin: 40px 0;
        position: relative;
        overflow: hidden;
    }
    
    .cta-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 102, 204, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    .cta-title {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
    }
    
    .cta-description {
        font-size: 16px;
        color: var(--text-secondary);
        margin-bottom: 24px;
        position: relative;
        z-index: 1;
    }

    /* Botão CTA customizado - estilos mais específicos para sobrescrever Streamlit */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0066CC 0%, #00B4D8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 32px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.4) !important;
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #003D99 0%, #0066CC 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.6) !important;
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }
    
    /* Benefit Card */
    .benefit-card {
        background: rgba(26, 31, 58, 0.4);
        border: 1px solid rgba(0, 102, 204, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER - HERO SECTION
# ============================================================================

st.markdown("""
<div class="hero-section">
    <div class="hero-title">⚙️ Data Driven Bearings</div>
    <div class="hero-subtitle">DDF Tech 2025</div>
    <div class="hero-description">
        Recomendador Inteligente de Rolamentos Industriais<br>
        Tecnologia de IA em Tempo Real • Análise Semântica Avançada
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# PROBLEMA VS SOLUÇÃO
# ============================================================================

st.markdown('<div class="section-title">🎯 O Desafio</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="problem-solution-card problem-card">
        <h3 style="color: #EF4444; margin-bottom: 20px;">❌ Problema Atual</h3>
        <p style="color: #E2E8F0; line-height: 1.8;">
            <strong>Técnicos perdem até 30 minutos</strong> navegando catálogos técnicos complexos:
        </p>
        <ul style="color: #94A3B8; line-height: 1.8; margin-top: 16px;">
            <li>📚 10.000+ produtos com especificações densas</li>
            <li>🔍 Busca manual por códigos e tabelas</li>
            <li>❓ Dúvidas sobre compatibilidade técnica</li>
            <li>⏰ Tempo desperdiçado em consultas repetitivas</li>
            <li>💸 Risco de especificar produto inadequado</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="problem-solution-card solution-card">
        <h3 style="color: #10B981; margin-bottom: 20px;">✅ Nossa Solução</h3>
        <p style="color: #E2E8F0; line-height: 1.8;">
            <strong>ML que entende linguagem natural</strong> e recomenda instantaneamente:
        </p>
        <ul style="color: #94A3B8; line-height: 1.8; margin-top: 16px;">
            <li>👾 Descreva o problema em português simples</li>
            <li>⚡ Resposta em menos de 3ms (sim, milissegundos!)</li>
            <li>🎯 Top 20 produtos com score de similaridade</li>
            <li>📊 Análise comparativa automatizada</li>
            <li>✅ 99.7% de qualidade nos dados técnicos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================================
# MÉTRICAS IMPRESSIONANTES
# ============================================================================

st.markdown("## 📈 Números que Impressionam")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">135K</div>
        <div class="stat-label">Registros Processados</div>
        <p style="font-size: 12px; color: #64748B; margin-top: 8px;">
            10K produtos + 5K clientes + 120K transações
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">99.7%</div>
        <div class="stat-label">Qualidade de Dados</div>
        <p style="font-size: 12px; color: #64748B; margin-top: 8px;">
            Validado com Soda Core
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">&lt;3ms</div>
        <div class="stat-label">Latência</div>
        <p style="font-size: 12px; color: #64748B; margin-top: 8px;">
            1.000+ requisições/segundo
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">100%</div>
        <div class="stat-label">Testes Passando</div>
        <p style="font-size: 12px; color: #64748B; margin-top: 8px;">
            9/9 testes automatizados
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================================
# BENEFÍCIOS POR PERSONA
# ============================================================================

st.markdown("## 👥 Benefícios por Perfil")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="benefit-card">
        <h4 style="color: #00B4D8; margin-bottom: 16px;">🔧 Técnicos</h4>
        <ul style="color: #E2E8F0; font-size: 14px; line-height: 1.8;">
            <li>Redução de 30min para <1s</li>
            <li>Recomendações precisas</li>
            <li>Menos erros de especificação</li>
            <li>Foco em análise crítica</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="benefit-card">
        <h4 style="color: #00B4D8; margin-bottom: 16px;">📊 Gestores</h4>
        <ul style="color: #E2E8F0; font-size: 14px; line-height: 1.8;">
            <li>Decisões data-driven</li>
            <li>Análise de custo-benefício</li>
            <li>KPIs de performance</li>
            <li>ROI mensurável</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="benefit-card">
        <h4 style="color: #00B4D8; margin-bottom: 16px;">💼 Vendas</h4>
        <ul style="color: #E2E8F0; font-size: 14px; line-height: 1.8;">
            <li>Conversão mais rápida</li>
            <li>Argumentação técnica</li>
            <li>Cross-sell inteligente</li>
            <li>Satisfação do cliente</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================================
# TIMELINE DE FASES
# ============================================================================
import streamlit as st

st.markdown("""
    <style>
    .roadmap-wrapper {
        display: flex;
        overflow-x: auto;
        padding: 40px 20px;
        background: rgba(26, 31, 58, 0.6);
        border: 1px solid rgba(0, 102, 204, 0.2);
        border-radius: 16px;
        gap: 0;
        scrollbar-width: thin;
    }
    
    .roadmap-wrapper::-webkit-scrollbar {
        height: 6px;
    }
    .roadmap-wrapper::-webkit-scrollbar-thumb {
        background: rgba(0, 102, 204, 0.5);
        border-radius: 10px;
    }

    .roadmap-step {
        min-width: 250px;
        flex: 1;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .roadmap-step::after {
        content: "";
        position: absolute;
        top: 15px;
        left: 50%;
        width: 100%;
        height: 2px;
        background: rgba(0, 102, 204, 0.3);
        z-index: 1;
    }

    .roadmap-step:last-child::after {
        display: none;
    }

    .roadmap-dot {
        width: 30px;
        height: 30px;
        background: #1A1F3A;
        border: 3px solid #0066CC;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 2;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(0, 102, 204, 0.6);
        color: white;
        font-size: 12px;
        font-weight: bold;
    }

    .roadmap-content h4 {
        color: #FFFFFF;
        font-size: 16px;
        margin-bottom: 8px !important;
    }

    .roadmap-content p {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.4;
        padding: 0 10px;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("## 🚀 Roadmap do Projeto")

col_main, col_side = st.columns([2, 1])
# 2. HTML do Roadmap Horizontal
st.markdown("""
    <div class="roadmap-wrapper">
        <div class="roadmap-step">
            <div class="roadmap-dot">1</div>
            <div class="roadmap-content">
                <h4>Fase 1-2: Fundação</h4>
                <p>✅ 135K registros  
99.7% qualidade</p>
            </div>
        </div>
        <div class="roadmap-step">
            <div class="roadmap-dot">2</div>
            <div class="roadmap-content">
                <h4>Fase 3-4: Features</h4>
                <p>✅ Star Schema  
12 features técnicas</p>
            </div>
        </div>
        <div class="roadmap-step">
            <div class="roadmap-dot">3</div>
            <div class="roadmap-content">
                <h4>Fase 5: Analytics</h4>
                <p>✅ 20+ visualizações  
6 insights</p>
            </div>
        </div>
        <div class="roadmap-step">
            <div class="roadmap-dot">4</div>
            <div class="roadmap-content">
                <h4>Fase 6: ML + API</h4>
                <p>✅ TF-IDF treinado  
API operacional</p>
            </div>
        </div>
        <div class="roadmap-step">
            <div class="roadmap-dot">5</div>
            <div class="roadmap-content">
                <h4>Fase 7: Data App</h4>
                <p>✅ Publicado no  
Streamlit Cloud</p>
            </div>
        </div>
        <div class="roadmap-step">
            <div class="roadmap-dot">6</div>
            <div class="roadmap-content">
                <h4>Fase 8: Monitoring</h4>
                <p>✅ Sistema de  
monitoramento ativo</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


st.divider()

# ============================================================================
# TECH STACK
# ============================================================================

st.markdown("## 🛠️ Tecnologias Utilizadas")

st.markdown("""
<div style="background: rgba(26, 31, 58, 0.6); border: 1px solid rgba(0, 102, 204, 0.2); 
            border-radius: 16px; padding: 32px; text-align: center;">
    <span class="tech-badge">🐍 Python 3.8+</span>
    <span class="tech-badge">📊 Pandas & NumPy</span>
    <span class="tech-badge">👾 Scikit-learn</span>
    <span class="tech-badge">⚡ FastAPI</span>
    <span class="tech-badge">🎨 Streamlit</span>
    <span class="tech-badge">📈 Matplotlib & Seaborn</span>
    <span class="tech-badge">✅ Pytest</span>
    <span class="tech-badge">🔍 TF-IDF</span>
    <span class="tech-badge">📦 Parquet</span>
    <span class="tech-badge">🔐 Soda Core</span>
    <span class="tech-badge">🚀 Uvicorn</span>
    <span class="tech-badge">📊 Cosine Similarity</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================================
# DOCUMENTAÇÃO
# ============================================================================

st.markdown("## 📚 Documentação Técnica")

REPO_URL = "https://github.com/Crys0231/CRYSLAYNE_CINARA_DDF_TECH_122025/tree/main"

docs = [
    ("📋 Planejamento", "docs/planejamento.md", "Roadmap completo das 8 fases"),
    ("🏗️ Arquitetura", "docs/arquitetura.md", "Stack técnica e padrões de design"),
    ("📊 Modelagem", "docs/modelagem_dados.md", "Star Schema e estruturas de dados"),
    ("📈 EDA", "docs/analytics-fase5.md", "20+ visualizações e 6 insights"),
    ("👾 Avaliação ML", "docs/avaliacao-fase6.md", "Performance do modelo TF-IDF"),
]

col1, col2 = st.columns([2, 1])

with col1:
    for name, path, desc in docs:
        st.markdown(f"""
        <div style="background: rgba(26, 31, 58, 0.4); border: 1px solid rgba(0, 102, 204, 0.15); 
                    border-radius: 12px; padding: 20px; margin-bottom: 12px; 
                    transition: all 0.3s ease;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color: #FFFFFF; margin: 0 0 8px 0;">{name}</h4>
                    <p style="color: #94A3B8; font-size: 13px; margin: 0;">{desc}</p>
                </div>
                <a href="{REPO_URL}/{path}" target="_blank" style="
                    background: linear-gradient(135deg, #0066CC 0%, #00B4D8 100%);
                    color: white;
                    text-decoration: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: 600;
                    white-space: nowrap;
                ">
                    Acessar →
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 180, 216, 0.1) 100%); 
                border: 1px solid rgba(0, 102, 204, 0.2); border-radius: 16px; padding: 24px; height: 100%;">
        <h4 style="color: #FFFFFF; margin-bottom: 20px;">📖 Recursos Extras</h4>
        <ul style="color: #E2E8F0; font-size: 14px; line-height: 2;">
            <li><a href="{REPO_URL}" target="_blank" style="color: #00B4D8;">🔗 Repositório GitHub</a></li>
            <li><a href="{REPO_URL}/README.md" target="_blank" style="color: #00B4D8;">📄 README</a></li>
            <li><a href="#" style="color: #00B4D8;">🎥 Demo em Vídeo (em breve)</a></li>
            <li><a href="#" style="color: #00B4D8;">📊 Apresentação (em breve)</a></li>
        </ul>
    </div>
    """.replace("{REPO_URL}", REPO_URL), unsafe_allow_html=True)

st.divider()


# ============================================================================
# CALL TO ACTION - SEÇÃO DESTACADA
# ============================================================================

st.markdown("""
<div class="cta-section">
    <div class="cta-title">🚀 Pronto para Começar?</div>
    <div class="cta-description">
        Acesse a página de <strong>Recomendações</strong> através do menu lateral e 
        descubra os rolamentos ideais para sua aplicação industrial em segundos.
    </div>
</div>
""", unsafe_allow_html=True)

# Container com padding negativo para posicionar botão dentro do card
st.markdown('<div style="margin-top: -60px; position: relative; z-index: 10; text-align: center;">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
with col2:
    if st.button(
        "📍 Ir para Recomendações →",
        use_container_width=True,
        key="cta_button",
        type="primary"
    ):
        st.switch_page("pages/recommendations.py")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ============================================================================
# FOOTER PROFISSIONAL
# ============================================================================

render_footer()