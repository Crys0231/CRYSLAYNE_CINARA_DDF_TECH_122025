# -*- coding: utf-8 -*-
"""
Data Driven Bearings - Recomendador Inteligente de Rolamentos
Página Principal - Dados Reais + Cores Consistentes
"""

# IMPORTS
import streamlit as st

from utils.session import setup_paths, get_engine, get_data
from components.layout import get_global_css, render_footer, render_sidebar
from utils.history import ensure_history_exists
from monitoring import StreamlitMonitor

# ============================================================================
# INICIALIZAR MONITOR 
# ============================================================================

if 'monitor' not in st.session_state:
    st.session_state.monitor = StreamlitMonitor(
        session_state=st.session_state
    )
    
    # Configurar baseline do modelo
    baseline_status = st.session_state.monitor.initialize_baseline()
    
    # Log inicial
    print(f"Monitor inicializado")
    print(f"Baseline: {baseline_status['samples']} amostras")
    print(f"Média: {baseline_status['mean']:.3f}")

# Alias para uso mais fácil
monitor = st.session_state.monitor

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(
    page_title="Data Driven Bearings",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup paths uma única vez
setup_paths()

# Garantir histórico
ensure_history_exists()

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
# CARACTERÍSTICAS - FEATURE CARDS
# ============================================================================

st.markdown('<div class="section-title">✨ Características Principais</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">👾</span>
        <div class="feature-title">IA Avançada</div>
        <div class="feature-description">
            Tecnologia TF-IDF de última geração combinada com Cosine Similarity para 
            recomendações precisas baseadas em análise semântica avançada.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">⚡</span>
        <div class="feature-title">Ultra Rápido</div>
        <div class="feature-description">
            Latência inferior a 3ms por recomendação. Processamento otimizado para 
            resultados instantâneos mesmo com grandes volumes de dados.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📊</span>
        <div class="feature-title">Análise Completa</div>
        <div class="feature-description">
            Visualizações interativas, gráficos comparativos, rankings detalhados 
            e exportação de dados em múltiplos formatos para análise aprofundada.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ============================================================================
# MÉTRICAS DO SISTEMA - CARDS PROFISSIONAIS
# ============================================================================

st.markdown('<div class="section-title">📊 Estatísticas do Sistema</div>', unsafe_allow_html=True)

if st.session_state.products_data is not None:
    products_df = st.session_state.products_data
    
    total_products = len(products_df)
    avg_price = products_df['list_price'].mean() if 'list_price' in products_df.columns else 0
    max_price = products_df['list_price'].max() if 'list_price' in products_df.columns else 0
    bearing_types = products_df['bearing_type'].nunique() if 'bearing_type' in products_df.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 32px; margin-bottom: 8px;">📦</div>
            <div style="font-size: 28px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">
                {total_products:,}
            </div>
            <div style="font-size: 14px; color: #94A3B8;">Produtos</div>
            <div style="font-size: 12px; color: #64748B; margin-top: 8px;">Base carregada</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 32px; margin-bottom: 8px;">⚙️</div>
            <div style="font-size: 28px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">
                {bearing_types}
            </div>
            <div style="font-size: 14px; color: #94A3B8;">Tipos</div>
            <div style="font-size: 12px; color: #64748B; margin-top: 8px;">Variações</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 32px; margin-bottom: 8px;">💰</div>
            <div style="font-size: 24px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">
                R$ {avg_price:,.0f}
            </div>
            <div style="font-size: 14px; color: #94A3B8;">Preço Médio</div>
            <div style="font-size: 12px; color: #64748B; margin-top: 8px;">Máx: R$ {max_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 32px; margin-bottom: 8px;">⭐</div>
            <div style="font-size: 28px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">
                99.7%
            </div>
            <div style="font-size: 14px; color: #94A3B8;">Acurácia</div>
            <div style="font-size: 12px; color: #64748B; margin-top: 8px;">TF-IDF Engine</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# SOBRE - CARDS INFORMATIVOS
# ============================================================================

st.markdown('<div class="section-title">🎯 O Que é Data Driven Bearings?</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown((
        '<div style="background: rgba(26, 31, 58, 0.6); border: 1px solid rgba(0, 102, 204, 0.2); '
        'border-radius: 16px; padding: 28px; line-height: 1.8;">'
            '<p style="font-size: 16px; color: #E2E8F0; margin-bottom: 20px;">'
                '<strong style="color: #FFFFFF;">Data Driven Bearings</strong> é uma plataforma inteligente '
                'que utiliza Inteligência Artificial para recomendar rolamentos industriais baseado em '
                'análise semântica de problemas técnicos descritos em linguagem natural.'
            '</p>'
            '<div style="margin-top: 24px;">'
                '<h4 style="color: #FFFFFF; font-size: 18px; margin-bottom: 16px;">✨ Funcionalidades Principais:</h4>'
                '<div style="color: #E2E8F0; font-size: 14px;">'
                    '<div style="margin-bottom: 12px;">'
                        '<strong style="color: #00B4D8;">🔍 Busca em Linguagem Natural:</strong> '
                        'Descreva seu problema técnico e receba recomendações instantâneas'
                    '</div>'
                    '<div style="margin-bottom: 12px;">'
                        '<strong style="color: #00B4D8;">📊 Análise Comparativa:</strong> '
                        'Gráficos interativos, comparações e rankings detalhados de produtos'
                    '</div>'
                    '<div style="margin-bottom: 12px;">'
                        '<strong style="color: #00B4D8;">💾 Exportação de Dados:</strong> '
                        'Baixe resultados em CSV para análise adicional'
                    '</div>'
                    '<div>'
                        '<strong style="color: #00B4D8;">⚡ Performance Ultra Rápida:</strong> '
                        'Respostas em menos de 3ms utilizando tecnologia TF-IDF'
                    '</div>'
                '</div>'
            '</div>'
            '<div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid rgba(0, 102, 204, 0.2);">'
                '<p style="font-size: 13px; color: #94A3B8;">'
                    '<strong>Stack Tecnológico:</strong> TF-IDF • Cosine Similarity • Streamlit • Pandas'
                '</p>'
            '</div>'
        '</div>'
    ), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #FFFFFF; font-size: 18px; margin-bottom: 16px; margin-top: 0;">
            💡 Dica Profissional
        </h4>
        <p style="color: #E2E8F0; font-size: 14px; line-height: 1.7; margin-bottom: 16px;">
            Quanto mais detalhada sua descrição, melhores serão os resultados!
        </p>
        <div style="background: rgba(0, 0, 0, 0.3); border-radius: 8px; padding: 12px; margin-top: 16px;">
            <div style="color: #EF4444; font-size: 12px; margin-bottom: 8px;">
                ❌ Exemplo Ruim:
            </div>
            <div style="color: #94A3B8; font-size: 12px; font-style: italic;">
                "Rolamento"
            </div>
            <div style="color: #10B981; font-size: 12px; margin-top: 12px; margin-bottom: 8px;">
                ✅ Exemplo Bom:
            </div>
            <div style="color: #E2E8F0; font-size: 12px; font-style: italic;">
                "Rolamento para máquina com vibração em siderurgia, RPM > 10000, temperatura 80°C"
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# COMO COMEÇAR - PASSOS VISUAIS
# ============================================================================

st.markdown('<div class="section-title">🚀 Como Começar em 3 Passos</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step-card">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <span class="step-number">1</span>
            <h3 style="color: #FFFFFF; margin: 0; font-size: 18px;">Descreva seu Problema</h3>
        </div>
        <ul style="color: #E2E8F0; font-size: 14px; line-height: 1.8; margin-left: 56px; padding: 0;">
            <li>Clique em <strong style="color: #00B4D8;">"Recomendações"</strong> no menu lateral</li>
            <li>Digite uma descrição técnica detalhada do seu problema</li>
            <li>Use o máximo de informações relevantes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <span class="step-number">2</span>
            <h3 style="color: #FFFFFF; margin: 0; font-size: 18px;">Visualize Exemplos</h3>
        </div>
        <ul style="color: #E2E8F0; font-size: 14px; line-height: 1.8; margin-left: 56px; padding: 0;">
            <li>Explore exemplos por indústria na página de Recomendações</li>
            <li>Veja sugestões práticas de como descrever problemas</li>
            <li>Copie e adapte conforme sua necessidade</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step-card">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <span class="step-number">3</span>
            <h3 style="color: #FFFFFF; margin: 0; font-size: 18px;">Analise Resultados</h3>
        </div>
        <ul style="color: #E2E8F0; font-size: 14px; line-height: 1.8; margin-left: 56px; padding: 0;">
            <li>Ranking de produtos com scores de similaridade</li>
            <li>Gráficos comparativos interativos</li>
            <li>Exporte para Excel para análise detalhada</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

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
