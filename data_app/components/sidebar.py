import streamlit as st

def render_sidebar():
    """Renderiza sidebar com filtros e configurações"""
    
    with st.sidebar:
        st.title("⚙️ Configurações")
        
        # Seção de filtros
        st.subheader("🔍 Filtros")
        
        price_range = st.slider(
            "Faixa de Preço (R$):",
            min_value=0,
            max_value=10000,
            value=(0, 10000),
            step=100
        )
        
        bearing_types = st.multiselect(
            "Tipos de Rolamento:",
            ["Autocompensador", "Esférico", "Cilíndrico", "Contato Angular", "Agujas"],
            default=None
        )
        
        industries = st.multiselect(
            "Indústrias:",
            ["Siderurgia", "Alimentos", "Mineração", "Energia", "Automotiva"],
            default=None
        )
        
        st.divider()
        
        # Informações gerais
        st.subheader("ℹ️ Sobre")
        
        st.caption("""
        **DDF Tech 2025** - Recomendador inteligente de rolamentos industriais
        
        - 🎯 Fases: 7 de 8 concluídas
        - ✅ Status: Production Ready
        - ⚡ Latência: <3ms
        - 📊 Data Quality: 99.7%
        """)
        
        st.divider()
        
        # Links úteis
        st.subheader("🔗 Links Úteis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("📖 Documentação", use_container_width=True)
        
        with col2:
            st.button("📧 Suporte", use_container_width=True)
        
        st.divider()
        
        # Versão
        st.caption("v2.0 • Janeiro 2026")
