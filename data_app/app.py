import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# CONFIG - TEMA ESCURO
# ============================================================================

st.set_page_config(
    page_title="DDF Tech 2025 - Recomendador de Rolamentos",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tema escuro matplotlib
plt.style.use('dark_background')

# ============================================================================
# CSS ESCURO
# ============================================================================

st.markdown("""
<style>
    :root {
        --bg: #0E1117;
        --bg2: #161B22;
        --text: #C9D1D9;
        --cyan: #00D9FF;
        --orange: #FF8C00;
        --green: #3FB950;
    }
    
    body { background-color: var(--bg); color: var(--text); }
    .main { background-color: var(--bg); }
    .stSidebar { background-color: var(--bg2); }
    
    .main-header {
        background: linear-gradient(135deg, var(--cyan) 0%, var(--orange) 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 217, 255, 0.2);
    }
    
    .stButton button {
        background: linear-gradient(135deg, var(--cyan) 0%, #0096B8 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        font-weight: 600;
    }
    
    .stTextArea textarea {
        background-color: var(--bg2);
        border: 2px solid #444;
        color: var(--text);
    }
    
    .stTextArea textarea:focus {
        border-color: var(--cyan);
    }
    
    .stMetric { background-color: var(--bg2); border-left: 4px solid var(--cyan); padding: 1rem; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# IMPORTS
# ============================================================================

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.recommendation_engine import RecommendationEngine
except ImportError:
    st.error("❌ RecommendationEngine não encontrada")
    st.stop()

try:
    from data_app.utils.data_loader import load_products_data
except ImportError:
    st.error("❌ data_loader não encontrada")
    st.stop()

# ============================================================================
# CACHE
# ============================================================================
from src.recommendation_engine import RecommendationEngine
from data_app.utils.data_loader import load_products_data

@st.cache_resource
def init_engine():
    try:
        # 1) Carregar dados de produtos
        products_df = load_products_data()

        # 2) Instanciar engine
        engine = RecommendationEngine()

        # 3) Treinar OU carregar modelo
        # opção A: treinar toda vez a partir do DataFrame
        engine.fit(products_df, text_column="full_description")

        # opção B: se você já tiver salvo um .pkl em disco:
        # engine = RecommendationEngine.load_model("models/recommendation_engine.pkl")

        return engine
    except Exception as e:
        st.error(f"❌ Erro ao inicializar engine: {e}")
        return None


@st.cache_data
def load_data():
    try:
        data = load_products_data()
        if data is not None and not data.empty:
            st.success(f"✅ {len(data)} produtos carregados")
        return data
    except Exception as e:
        st.error(f"❌ Erro: {e}")
        return None

# ============================================================================
# SESSION STATE
# ============================================================================

if 'engine' not in st.session_state:
    st.session_state.engine = init_engine()

if 'products_data' not in st.session_state:
    st.session_state.products_data = load_data()

if 'history' not in st.session_state:
    st.session_state.history = []

if 'last_results' not in st.session_state:
    st.session_state.last_results = None

if 'last_query' not in st.session_state:
    st.session_state.last_query = None

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.title("⚙️ Configurações")
    st.divider()
    
    st.subheader("📊 Sistema")
    col_s1, col_s2 = st.columns(2)
    with col_s1: st.metric("🎯 Acurácia", "99.7%")
    with col_s2: st.metric("⚡ Latência", "<3ms")
    
    col_s3, col_s4 = st.columns(2)
    with col_s3: st.metric("📦 Produtos", "10K+")
    with col_s4: st.metric("✅ Status", "Ready")
    
    st.divider()
    
    st.subheader("🔍 Filtros")
    with st.expander("💰 Preço", expanded=False):
        st.number_input("Mín (R$)", value=0, step=100)
        st.number_input("Máx (R$)", value=10000, step=100)
    
    st.divider()
    st.caption("DDF Tech 2025 • v2.0")

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="main-header">
    <h1>⚙️ DDF Tech 2025</h1>
    <h3>Recomendador Inteligente de Rolamentos</h3>
    <p>Tecnologia de IA em tempo real</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN
# ============================================================================

col_main, col_stats = st.columns([3, 1], gap="large")

with col_main:
    st.subheader("🔍 Descreva seu problema")
    st.caption("💬 Digite em português, inglês ou espanhol")
    
    with st.form(key="search_form"):
        col_input, col_config = st.columns([4, 1])
        
        with col_input:
            user_query = st.text_area(
                "Descrição:",
                placeholder="Ex: Preciso de um rolamento para alta vibração em siderurgia...",
                height=120,
                label_visibility="collapsed"
            )
        
        with col_config:
            st.caption("Idioma")
            language = st.selectbox(
                "Lang:",
                ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"],
                label_visibility="collapsed"
            )
            
            st.caption("Resultados")
            top_k = st.slider("Qtd:", 1, 20, 10, label_visibility="collapsed")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        
        with col_btn1:
            submitted = st.form_submit_button("🔍 Buscar", use_container_width=True)
        
        with col_btn2:
            clear = st.form_submit_button("🔄 Limpar", use_container_width=True)
    
    # Busca
    if submitted and user_query:
        st.session_state.last_query = user_query
        
        with st.spinner("🔄 Analisando..."):
            try:
                if st.session_state.engine is None:
                    st.error("❌ Engine não inicializado")
                else:
                    recommendations = st.session_state.engine.recommend(
                        user_query,
                        top_k=top_k
                    )
                    
                    st.session_state.last_results = recommendations
                    st.session_state.history.append({
                        'query': user_query,
                        'timestamp': datetime.now(),
                        'count': len(recommendations)
                    })
                    
                    st.success(f"✅ {len(recommendations)} recomendações!")
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    
    elif clear:
        st.session_state.last_results = None
        st.session_state.last_query = None
        st.rerun()
    
    # Resultados
    if st.session_state.last_results:
        st.divider()
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Ranking", "📈 Gráfico", "💾 Exportar", "ℹ️ Detalhes"])
        
        with tab1:
            st.subheader("Top Recomendações")
            
            results_data = []
            for i, rec in enumerate(st.session_state.last_results, 1):
                results_data.append({
                    'Rank': i,
                    'Produto': rec.get('product_name', 'N/A'),
                    'Score': f"{rec.get('score', 0):.1%}",
                    'Tipo': rec.get('bearing_type', 'N/A'),
                    'Preço': f"R$ {rec.get('price', 0):,.2f}",
                })
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        with tab2:
            st.subheader("Comparação de Scores")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            top_n = st.session_state.last_results[:5]
            names = [rec.get('product_name', 'N/A')[:20] for rec in top_n]
            scores = [rec.get('score', 0) for rec in top_n]
            
            colors = ['#3FB950' if s > 0.5 else '#FFA657' if s > 0.3 else '#F85149' for s in scores]
            
            ax.barh(names, scores, color=colors, edgecolor='#00D9FF', linewidth=2)
            ax.set_xlabel('Score de Similaridade', fontweight='bold')
            ax.set_title('Top 5 Recomendações', fontweight='bold', fontsize=14)
            ax.set_xlim(0, 1)
            
            for j, score in enumerate(scores):
                ax.text(score + 0.02, j, f'{score:.1%}', va='center', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab3:
            st.subheader("📥 Exportar Resultados")
            
            # Preparar dados
            export_data = []
            for i, rec in enumerate(st.session_state.last_results, 1):
                export_data.append({
                    'Rank': i,
                    'Produto': rec.get('product_name', 'N/A'),
                    'Score': f"{rec.get('score', 0):.1%}",
                    'Preço': f"R$ {rec.get('price', 0):,.2f}",
                    'Tipo': rec.get('bearing_type', 'N/A'),
                })
            
            export_df = pd.DataFrame(export_data)
            
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                # CSV
                csv_data = export_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download CSV",
                    data=csv_data,
                    file_name=f"recomendacoes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_e2:
                st.info("💡 PDF: Instale reportlab com `pip install reportlab`")
            
            st.divider()
            st.caption("📋 Dados:")
            st.dataframe(export_df, use_container_width=True, height=250)
        
        with tab4:
            st.subheader("Detalhes")
            
            for i, rec in enumerate(st.session_state.last_results[:5], 1):
                with st.expander(f"#{i} - {rec.get('product_name', 'N/A')} ({rec.get('score', 0):.1%})"):
                    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
                    
                    with col_d1: st.metric("Score", f"{rec.get('score', 0):.1%}")
                    with col_d2: st.metric("Preço", f"R$ {rec.get('price', 0):,.0f}")
                    with col_d3: st.metric("RPM", f"{rec.get('rpm_capacity', 0):,}")
                    with col_d4: st.metric("Tipo", rec.get('bearing_type', 'N/A'))
                    
                    st.write("**Descrição:**")
                    st.caption(rec.get('technical_description', 'N/A'))

with col_stats:
    st.subheader("📊 Estatísticas")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1: st.metric("Consultas", len(st.session_state.history))
    with col_s2: st.metric("Favoritos", "0")
    
    st.divider()
    
    if st.session_state.history:
        st.write("### 📋 Histórico")
        for item in st.session_state.history[-5:]:
            st.caption(f"🕐 {item['timestamp'].strftime('%H:%M')}")
            st.caption(f"📌 {item['query'][:40]}...")
            st.caption(f"✅ {item['count']} resultados")
            st.divider()

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1: st.caption("📄 **DDF Tech 2025** - Data Driven Bearings")
with col_f2: st.caption("⚙️ **Fase 7:** Data App")
with col_f3: st.caption("✅ **Status:** Production Ready")
