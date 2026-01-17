import streamlit as st
from datetime import datetime

def render_header():
    """Renderiza cabeçalho da aplicação"""
    
    st.markdown("""
    <div class="header-section">
        <h1>⚙️ Data Driven Bearings</h1>
        <h3>DDF Tech 2025</h3>
        <p>Recomendador Inteligente de Rolamentos Industriais • Tecnologia de IA para recomendações precisas em tempo real</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Informações do sistema
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Acurácia", "99.7%")
    
    with col2:
        st.metric("⚡ Latência", "<3ms")
    
    with col3:
        st.metric("📦 Produtos", "10.000+")
    
    with col4:
        st.metric("🔄 Versão", "2.0")
