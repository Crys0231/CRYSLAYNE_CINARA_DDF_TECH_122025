"""
Página inicial da aplicação
"""

import streamlit as st

def render_home():
    """Renderiza página inicial"""
    
    st.title("🏠 Bem-vindo ao DDF Tech 2025")
    
    st.markdown("""
    ### Recomendador Inteligente de Rolamentos Industriais
    
    Bem-vindo à plataforma que transforma suas descrições de problemas 
    em recomendações precisas de rolamentos em tempo real.
    """)
    
    # Seções principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 🚀 Rápido
        Recomendações em **<3ms**
        
        Respostas instantâneas alimentadas por IA
        """)
    
    with col2:
        st.success("""
        ### 🎯 Preciso
        **99.7%** de qualidade de dados
        
        Baseado em 135K registros validados
        """)
    
    with col3:
        st.warning("""
        ### 💡 Inteligente
        Análise **semântica** avançada
        
        Entende sua descrição naturalmente
        """)
    
    st.divider()
    
    # Como usar
    st.subheader("📖 Como Usar")
    
    step1, step2, step3 = st.columns(3)
    
    with step1:
        st.markdown("""
        **1. Descreva seu problema**
        
        Use linguagem natural em português, 
        inglês ou espanhol.
        """)
    
    with step2:
        st.markdown("""
        **2. Clique em Buscar**
        
        O motor de IA processará sua 
        descrição instantaneamente.
        """)
    
    with step3:
        st.markdown("""
        **3. Receba Recomendações**
        
        Ranking dos melhores rolamentos 
        para sua aplicação.
        """)
    
    st.divider()
    
    # Exemplos
    st.subheader("💡 Exemplos de Uso")
    
    examples = [
        {
            'title': 'Siderurgia - Alta Vibração',
            'query': 'Preciso de um rolamento que suporte alta vibração em um compressor de ar para aplicação em siderurgia',
            'industry': '🏭 Siderurgia'
        },
        {
            'title': 'Alimentos - Limpeza Frequente',
            'query': 'Rolamento para máquina de envasamento que recebe limpeza frequente com água',
            'industry': '🍱 Alimentos'
        },
        {
            'title': 'Automotiva - Alta Velocidade',
            'query': 'Rolamento para transmissão automática que opera em alta velocidade e temperatura constante',
            'industry': '🚗 Automotiva'
        },
    ]
    
    for example in examples:
        with st.expander(f"📌 {example['title']}"):
            st.caption(example['industry'])
            st.write(example['query'])
    
    st.divider()
    
    # Estatísticas
    st.subheader("📊 Estatísticas do Sistema")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("🎯 Acurácia", "99.7%")
    
    with col_stat2:
        st.metric("⚡ Latência", "<3ms")
    
    with col_stat3:
        st.metric("📦 Produtos", "10.000+")
    
    with col_stat4:
        st.metric("🔄 Versão", "2.0")
    
    st.divider()
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px;">
        <h3>🚀 Pronto para começar?</h3>
        <p>Acesse a aba <strong>Recomendações</strong> e descreva seu problema!</p>
    </div>
    """, unsafe_allow_html=True)

# Renderizar se executado diretamente
if __name__ == "__main__":
    render_home()
