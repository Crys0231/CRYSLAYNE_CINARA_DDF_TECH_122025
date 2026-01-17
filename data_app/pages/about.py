"""
Página Sobre - Redesenhada com Storytelling
"""

import streamlit as st
import sys
import os

# IMPORTS
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


try:
    from data_app.components.sidebar import render_sidebar
    from src.recommendation_engine import RecommendationEngine
    from data_app.utils.data_loader import load_products_data
    from data_app.components.layout import (
        get_global_css, 
        render_header, 
        render_footer,
        render_custom_divider
    )
    from monitoring.alert_manager import AlertManager
except ImportError as e:
    st.warning(f"⚠️ Alguns módulos não foram importados: {e}")

# ============================================================================
# CACHE E INICIALIZAÇÃO
# ============================================================================

@st.cache_resource
def init_engine():
    """Inicializa a engine de recomendação"""
    try:
        products_df = load_products_data()
        if products_df is None or products_df.empty:
            st.error("❌ Erro: Dados de produtos não encontrados")
            return None
        engine = RecommendationEngine()
        engine.fit(products_df, text_column="full_description")
        return engine
    except Exception as e:
        st.error(f"❌ Erro ao inicializar engine: {e}")
        return None

@st.cache_data
def load_data():
    """Carrega os dados de produtos"""
    try:
        return load_products_data()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None

# ============================================================================
# SESSION STATE - INICIALIZAÇÃO DA ENGINE
# ============================================================================

# Inicializar engine se não existir
if 'engine' not in st.session_state or st.session_state.engine is None:
    with st.spinner("⚙️ Inicializando sistema de recomendação..."):
        st.session_state.engine = init_engine()

# Inicializar dados se não existir
if 'products_data' not in st.session_state or st.session_state.products_data is None:
    st.session_state.products_data = load_data()

# Validação crítica - parar execução se engine não foi inicializada
if st.session_state.engine is None:
    st.error("❌ Sistema não inicializado. Por favor, volte à página inicial.")
    st.stop()

# CONFIG
st.set_page_config(page_title="Sobre o Projeto", layout="wide")

# APLICAR ESTILO GLOBAL
st.markdown(get_global_css(), unsafe_allow_html=True)

# SIDEBAR
render_sidebar()

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
            <strong>IA que entende linguagem natural</strong> e recomenda instantaneamente:
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

st.markdown("## 🚀 Roadmap do Projeto")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="background: rgba(26, 31, 58, 0.6); border: 1px solid rgba(0, 102, 204, 0.2); border-radius: 16px; padding: 32px;">
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <h4 style="color: #FFFFFF; margin-bottom: 8px;">Fase 1-2: Fundação de Dados</h4>
            <p style="color: #94A3B8; font-size: 14px;">✅ 135K registros gerados + 99.7% qualidade validada</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <h4 style="color: #FFFFFF; margin-bottom: 8px;">Fase 3-4: Transformação & Features</h4>
            <p style="color: #94A3B8; font-size: 14px;">✅ Star Schema implementado + 12 features técnicas</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <h4 style="color: #FFFFFF; margin-bottom: 8px;">Fase 5: Analytics (EDA)</h4>
            <p style="color: #94A3B8; font-size: 14px;">✅ 20+ visualizações + 6 insights estratégicos</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot"></div>
            <h4 style="color: #FFFFFF; margin-bottom: 8px;">Fase 6: ML Model + API</h4>
            <p style="color: #94A3B8; font-size: 14px;">✅ TF-IDF treinado + API REST operacional</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot pending"></div>
            <h4 style="color: #FFFFFF; margin-bottom: 8px;">Fase 7: Data App (Atual)</h4>
            <p style="color: #94A3B8; font-size: 14px;">🔄 Interface Streamlit em desenvolvimento</p>
        </div>
        <div class="timeline-item">
            <div class="timeline-dot pending"></div>
            <h4 style="color: #FFFFFF; margin-bottom: 8px;">Fase 8: Monitoring (Próximo)</h4>
            <p style="color: #94A3B8; font-size: 14px;">📅 Planejado para 20-24/01/2026</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 180, 216, 0.1) 100%); border: 1px solid rgba(0, 102, 204, 0.2); border-radius: 16px; padding: 24px;">
        <h4 style="color: #FFFFFF; margin-bottom: 20px;">📊 Status Geral</h4>
        <div style="margin-bottom: 20px;">
            <p style="color: #94A3B8; font-size: 12px; margin-bottom: 8px;">PROGRESSO</p>
            <div style="background: rgba(0, 0, 0, 0.3); border-radius: 8px; height: 24px; position: relative;">
                <div style="background: linear-gradient(90deg, #0066CC, #00B4D8); width: 75%; height: 100%; border-radius: 8px;"></div>
                <span style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: 600; font-size: 12px;">75%</span>
            </div>
        </div>
        <div style="margin-top: 24px;">
            <p style="color: #10B981; font-size: 14px; margin-bottom: 8px;">✅ 6/8 Fases Concluídas</p>
            <p style="color: #F59E0B; font-size: 14px; margin-bottom: 8px;">🔄 1/8 Em Desenvolvimento</p>
            <p style="color: #94A3B8; font-size: 14px;">📅 1/8 Planejada</p>
        </div>
        <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid rgba(0, 102, 204, 0.2);">
            <p style="color: #00B4D8; font-weight: 600; font-size: 14px;">PRODUCTION READY</p>
            <p style="color: #64748B; font-size: 12px; margin-top: 8px;">Fases 1-6 operacionais</p>
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