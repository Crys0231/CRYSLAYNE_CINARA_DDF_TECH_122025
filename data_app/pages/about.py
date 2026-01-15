"""
Página Sobre
"""

import streamlit as st

def render_about():
    """Renderiza página sobre"""
    
    st.title("ℹ️ Sobre DDF Tech 2025")
    
    st.markdown("""
    ### Data Driven Bearings
    
    Plataforma inteligente de recomendação de rolamentos industriais que utiliza
    tecnologias avançadas de análise de dados e machine learning.
    """)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🎯 Missão")
        st.caption("""
        Revolucionar a forma como indústrias 
        selecionam rolamentos através de 
        inteligência artificial e análise semântica.
        """)
    
    with col2:
        st.subheader("🚀 Visão")
        st.caption("""
        Ser a plataforma líder em recomendações
        inteligentes para componentes industriais.
        """)
    
    with col3:
        st.subheader("💡 Valores")
        st.caption("""
        Precisão, Inovação, Confiabilidade
        e Excelência em Dados.
        """)
    
    st.divider()
    
    st.subheader("📊 Projeto DDF Tech 2025")
    
    st.markdown("""
    | Aspecto | Detalhes |
    |---------|----------|
    | **Status** | ✅ Fases 1-6 Production Ready |
    | **Datasets** | 135K registros validados |
    | **Data Quality** | 99.7% conformidade |
    | **Latência** | <3ms por recomendação |
    | **Modelo** | TF-IDF + Cosine Similarity |
    | **API** | FastAPI operacional |
    | **Testes** | 100% cobertura (9/9 passando) |
    """)
    
    st.divider()
    
    st.subheader("👥 Time")
    
    st.markdown("""
    - **Coordenador:** Cryslayne Cinara
    - **Tech Lead:** Cryslayne Cinara
    - **Data Engineer:** Cryslayne Cinara
    - **ML Engineer:** Cryslayne Cinara
    """)
    
    st.divider()
    
    st.subheader("📚 Documentação")
    
    docs = [
        ("📋 Planejamento", "docs/planejamento.md"),
        ("🏗️ Arquitetura", "docs/arquitetura.md"),
        ("📊 Modelagem", "docs/modelagem_dados.md"),
        ("📈 EDA", "docs/analytics-fase5.md"),
        ("🤖 Avaliação", "docs/avaliacao-fase6.md"),
    ]
    
    for name, path in docs:
        st.caption(f"📄 {name} - `{path}`")
    
    st.divider()
    
    st.subheader("📞 Suporte")
    
    col_sup1, col_sup2 = st.columns(2)
    
    with col_sup1:
        st.button("📧 Email", use_container_width=True)
    
    with col_sup2:
        st.button("💬 Suporte", use_container_width=True)
    
    st.divider()
    
    st.caption("**DDF Tech 2025** | v2.0 | Janeiro 2026")

# Renderizar se executado diretamente
if __name__ == "__main__":
    render_about()
