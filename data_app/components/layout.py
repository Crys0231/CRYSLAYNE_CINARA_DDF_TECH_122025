"""
Layout.py - Design do site, padronizado para as páginas
"""

import streamlit as st
from datetime import datetime

# ============================================================================
# CSS GLOBAL - DESIGN MODERNO PADRONIZADO
# ============================================================================

def get_global_css():
    """
    CSS global com design moderno padronizado.
    Baseado no estilo do app.py com cores azuis e gradientes escuros.
    """
    return """
    <style>
    /* Importação de fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* ==================== VARIÁVEIS CSS ==================== */
    :root {
        --primary: #0066CC;
        --primary-dark: #003D99;
        --secondary: #00B4D8;
        --success: #10B981;
        --warning: #FFA421;
        --error: #EF4444;
        --text-primary: #FFFFFF;
        --text-secondary: #E2E8F0;
        --text-muted: #94A3B8;
        --bg-gradient: linear-gradient(135deg, #0F172A 0%, #1A1F3A 100%);
        --card-bg: rgba(26, 31, 58, 0.6);
        --border-color: rgba(0, 102, 204, 0.2);
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 12px rgba(0, 102, 204, 0.15);
        --shadow-lg: 0 8px 24px rgba(0, 102, 204, 0.2);
    }

    /* Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* ==================== TIPOGRAFIA ==================== */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        font-family: 'Inter', sans-serif !important;
    }

    h1 { font-size: 2rem !important; margin-bottom: 1rem !important; }
    h2 { font-size: 1.5rem !important; margin-bottom: 0.875rem !important; }
    h3 { font-size: 1.25rem !important; margin-bottom: 0.75rem !important; }

    p { 
        color: var(--text-secondary) !important;
        line-height: 1.6 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ==================== HERO SECTION ==================== */
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px 20px;
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 180, 216, 0.05) 100%);
        border-radius: 16px;
        margin-bottom: 32px;
        border: 1px solid var(--border-color);
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, #0066CC 0%, #00B4D8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        letter-spacing: -1px;
        line-height: 1.1;
        font-family: 'Inter', sans-serif;
    }
    
    .hero-subtitle {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-secondary);
        margin: 8px 0;
        font-family: 'Inter', sans-serif;
    }
    
    .hero-description {
        font-size: 16px;
        color: var(--text-muted);
        margin-top: 12px;
        line-height: 1.6;
        font-family: 'Inter', sans-serif;
    }

    /* ==================== CARDS MODERNOS ==================== */
    .modern-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 28px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        height: 100%;
    }

    .modern-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 102, 204, 0.4);
        box-shadow: 0 12px 32px rgba(0, 102, 204, 0.15);
    }

    .feature-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 28px;
        height: 100%;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 102, 204, 0.4);
        box-shadow: 0 12px 32px rgba(0, 102, 204, 0.15);
    }
    
    .feature-icon {
        font-size: 40px;
        margin-bottom: 16px;
        display: block;
    }
    
    .feature-title {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 12px;
        font-family: 'Inter', sans-serif;
    }
    
    .feature-description {
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.6;
        font-family: 'Inter', sans-serif;
    }

    .modern-card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }

    .modern-card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        font-family: 'Inter', sans-serif;
    }

    .modern-card-body {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.6;
        font-family: 'Inter', sans-serif;
    }

    /* ==================== MÉTRICAS ==================== */
    .metric-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(0, 102, 204, 0.3);
        box-shadow: 0 8px 24px rgba(0, 102, 204, 0.1);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        line-height: 1;
        font-family: 'Inter', sans-serif;
    }

    .metric-label {
        font-size: 0.875rem;
        color: var(--text-muted);
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    .metric-delta {
        font-size: 0.875rem;
        margin-top: 0.5rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    .metric-delta.positive { color: var(--success); }
    .metric-delta.negative { color: var(--error); }

    /* ==================== HEADER MODERNO ==================== */
    .modern-header {
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.05) 0%, rgba(0, 180, 216, 0.05) 100%);
        border-bottom: 2px solid var(--border-color);
        padding: 2rem 0 2rem 2rem;
        margin-bottom: 2rem;
        border-radius: 16px;
    }

    .header-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        line-height: 1.2;
        font-family: 'Inter', sans-serif;
    }

    .header-subtitle {
        font-size: 1rem;
        color: var(--text-muted);
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }

    /* ==================== STEP CARDS ==================== */
    .step-card {
        background: var(--card-bg);
        border-left: 4px solid var(--primary);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    
    .step-card:hover {
        background: rgba(0, 102, 204, 0.05);
        transform: translateX(4px);
    }
    
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        border-radius: 50%;
        color: white;
        font-weight: 700;
        font-size: 18px;
        margin-right: 16px;
        font-family: 'Inter', sans-serif;
    }

    /* ==================== SECTION TITLES ==================== */
    .section-title {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 32px 0 24px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid var(--border-color);
        font-family: 'Inter', sans-serif;
    }

    /* ==================== INFO BOX ==================== */
    .info-box {
        background: rgba(0, 180, 216, 0.1);
        border-left: 4px solid var(--secondary);
        border-radius: 12px;
        padding: 24px;
        margin: 24px 0;
    }

    /* ==================== CTA SECTION ==================== */
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
        font-family: 'Inter', sans-serif;
    }
    
    .cta-description {
        font-size: 16px;
        color: var(--text-secondary);
        margin-bottom: 24px;
        position: relative;
        z-index: 1;
        font-family: 'Inter', sans-serif;
    }

    /* ==================== BADGES ==================== */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.375rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        gap: 0.375rem;
        font-family: 'Inter', sans-serif;
    }

    .badge-primary {
        background: rgba(0, 102, 204, 0.2);
        color: var(--primary);
    }

    .badge-success {
        background: rgba(16, 185, 129, 0.2);
        color: var(--success);
    }

    .badge-warning {
        background: rgba(255, 164, 33, 0.2);
        color: var(--warning);
    }

    .badge-error {
        background: rgba(239, 68, 68, 0.2);
        color: var(--error);
    }

    .badge-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ==================== BOTÕES ==================== */
    .stButton > button {
        background: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button:hover {
        background: var(--primary-dark) !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px);
    }

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
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #003D99 0%, #0066CC 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.6) !important;
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }

    /* ==================== INPUTS ==================== */
    input, textarea, select {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.625rem !important;
        transition: all 0.2s ease !important;
        font-family: 'Inter', sans-serif !important;
    }

    input:focus, textarea:focus, select:focus {
        border-color: var(--primary) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.2) !important;
    }

    /* ==================== DATAFRAMES ==================== */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        overflow: hidden;
    }

    /* ==================== TABS ==================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 1px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--text-muted) !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px 8px 0 0 !important;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif !important;
    }

    .stTabs [aria-selected="true"] {
        background: var(--card-bg) !important;
        color: var(--primary) !important;
        border-bottom: 2px solid var(--primary) !important;
    }

    /* ==================== ALERTS ==================== */
    .stAlert {
        border-radius: 8px !important;
        border-left-width: 4px !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ==================== SIDEBAR ==================== */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid var(--border-color) !important;
    }

    /* ==================== FOOTER ==================== */
    .modern-footer {
        background: rgba(26, 31, 58, 0.4);
        border-top: 1px solid var(--border-color);
        padding: 2rem 0;
        margin-top: 3rem;
        text-align: center;
        border-radius: 16px;
    }

    .footer-text {
        color: var(--text-muted);
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif;
    }

    .footer-link {
        color: var(--primary);
        text-decoration: none;
        transition: color 0.2s ease;
    }

    .footer-link:hover {
        color: var(--secondary);
    }

    /* ==================== DIVIDER ==================== */
    .modern-divider {
        border: none;
        border-top: 1px solid var(--border-color);
        margin: 2rem 0;
    }

    /* ==================== CUSTOM DIVIDER ==================== */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(0, 102, 204, 0.3) 50%, 
            transparent 100%);
        margin: 40px 0;
        border: none;
    }

    /* ==================== RESPONSIVIDADE ==================== */
    @media (max-width: 768px) {
        .header-title { font-size: 1.5rem; }
        .hero-title { font-size: 32px; }
        .metric-value { font-size: 1.5rem; }
        .modern-card { padding: 1rem; }
        .feature-card { padding: 1.5rem; }
    }

    /* ==================== SCROLLBAR ==================== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(0, 102, 204, 0.3);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 102, 204, 0.5);
    }
    </style>
    """

# ============================================================================
# COMPONENTES REUTILIZÁVEIS
# ============================================================================
def render_sidebar():
    """Renderiza sidebar profissional com Contato e Documentação"""
    
    with st.sidebar:
        # Logo e Título
        
        st.markdown("### ⚙️ **Data Driven Bearings**")
        st.markdown("*DDF Tech 2025*")
        st.divider()
        
        # Status do Sistema
        if 'engine' in st.session_state and st.session_state.engine:
            st.success("**Sistema Online**", icon="✅")
        else:
            st.error("Sistema Offline", icon="❌")
        
        st.divider()
        
        # Seção de Contato
        st.markdown("### 📞 **Suporte Técnico**")
        st.caption("📧 Email: cryslaynecinara0231@gmail.com")
        st.caption("📱 WhatsApp: +55 11 99859-0590")
        st.caption("🕐 Seg-Sex: 08h-18h (Brasília)")
        
        st.divider()
        
        # Seção de Documentação
        st.markdown("### 📚 **Documentação**")
        st.caption("[📖 Repo GitHub](https://github.com/Crys0231/CRYSLAYNE_CINARA_DDF_TECH_122025)")
        st.caption("[🎥 Vídeo Tutorial](https://youtube.com/@ddftech)")
        st.caption("🐛 [Reportar Bug](mailto:cryslaynecinara0231@gmail.com?subject=Bug%20Report%20-%20Data%20Driven%20Bearings)") 
        
        st.divider()
        
        # Footer
        st.caption("Data Driven Bearings • v3.2")
        st.caption(f"*Atualizado em {datetime.now().strftime('%d/%m/%Y')}*")

def render_header(title: str, subtitle: str = None, icon: str = None):
    """
    Renderiza header moderno e limpo.
    
    Args:
        title: Título principal
        subtitle: Subtítulo descritivo
        icon: Emoji/ícone (opcional)
    """
    icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ''
    subtitle_html = f'<div class="header-subtitle">{subtitle}</div>' if subtitle else ''
    
    st.markdown(f"""
    <div class="modern-header">
        <div class="header-title">{icon_html}{title}</div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, delta: str = None, icon: str = None):
    """
    Renderiza card de métrica moderno.
    
    Args:
        label: Rótulo da métrica
        value: Valor principal
        delta: Variação (ex: "+10%")
        icon: Emoji/ícone
    """
    icon_html = f'<div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''
    
    delta_class = ''
    if delta:
        if delta.startswith('+'):
            delta_class = 'positive'
        elif delta.startswith('-'):
            delta_class = 'negative'
    
    delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>' if delta else ''
    
    st.markdown(f"""
    <div class="metric-card">
        {icon_html}
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_card(title: str, content: str, icon: str = None):
    """
    Renderiza card genérico moderno.
    
    Args:
        title: Título do card
        content: Conteúdo HTML
        icon: Emoji/ícone
    """
    icon_html = f'<span style="font-size: 1.25rem;">{icon}</span>' if icon else ''
    
    st.markdown(f"""
    <div class="modern-card">
        <div class="modern-card-header">
            {icon_html}
            <div class="modern-card-title">{title}</div>
        </div>
        <div class="modern-card-body">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_badge(text: str, type: str = 'primary'):
    """
    Renderiza badge inline.
    
    Args:
        text: Texto do badge
        type: Tipo (primary, success, warning, error)
    """
    return f'<span class="badge badge-{type}">{text}</span>'


def render_divider():
    """Renderiza divisor moderno."""
    st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)

def render_custom_divider():
    """Renderiza divisor customizado com gradiente."""
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


def render_footer():
    """Renderiza footer moderno padronizado."""
    current_year = datetime.now().year
    
    st.markdown(f"""
    <div style="
        text-align: center; 
        padding: 32px 20px; 
        background: rgba(26, 31, 58, 0.4);
        border-radius: 16px;
        border: 1px solid rgba(0, 102, 204, 0.1);
        margin-top: 24px;
    ">
        <p style="color: #94A3B8; font-size: 14px; margin-bottom: 12px; font-family: 'Inter', sans-serif;">
            © {current_year} <strong style="color: #FFFFFF;">Data Driven Bearings</strong> • 
            Transformando recomendações em decisões inteligentes
        </p>
        <p style="color: #64748B; font-size: 11px; margin-top: 8px; font-family: 'Inter', sans-serif;">
            Desenvolvido com ❤️ por Cryslayne Cinara
        </p>
        <div style="
            display: flex; 
            justify-content: center; 
            gap: 24px; 
            margin-top: 16px;
            flex-wrap: wrap;
        ">
            <span style="color: #64748B; font-size: 12px; font-family: 'Inter', sans-serif;">Python</span>
            <span style="color: #64748B; font-size: 12px;">•</span>
            <span style="color: #64748B; font-size: 12px; font-family: 'Inter', sans-serif;">Streamlit</span>
            <span style="color: #64748B; font-size: 12px;">•</span>
            <span style="color: #64748B; font-size: 12px; font-family: 'Inter', sans-serif;">TF-IDF</span>
            <span style="color: #64748B; font-size: 12px;">•</span>
            <span style="color: #64748B; font-size: 12px; font-family: 'Inter', sans-serif;">Pandas</span>
            <span style="color: #64748B; font-size: 12px;">•</span>
            <span style="color: #64748B; font-size: 12px; font-family: 'Inter', sans-serif;">Machine Learning</span>
        </div>
    </div>
    """, unsafe_allow_html=True)



# ============================================================================
# CONFIGURAÇÃO DE TEMA
# ============================================================================

THEME_CONFIG = {
    'primary_color': '#0066CC',
    'primary_dark': '#003D99',
    'secondary_color': '#00B4D8',
    'success_color': '#10B981',
    'warning_color': '#FFA421',
    'error_color': '#EF4444',
    'background_color': '#0F172A',
    'card_background': 'rgba(26, 31, 58, 0.6)',
    'text_primary': '#FFFFFF',
    'text_secondary': '#E2E8F0',
    'text_muted': '#94A3B8',
    'border_color': 'rgba(0, 102, 204, 0.2)',
    'font': 'Inter, sans-serif'
}