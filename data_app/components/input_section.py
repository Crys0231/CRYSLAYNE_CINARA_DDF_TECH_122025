import streamlit as st

def render_input_section():
    """Renderiza seção de input de query"""
    
    # Abas para diferentes tipos de input
    tab1, tab2, tab3 = st.tabs(["📝 Texto Livre", "🎯 Templates", "⚡ Exemplos"])
    
    with tab1:
        user_query = st.text_area(
            "Digite seu problema:",
            placeholder="Ex: Preciso de um rolamento para aplicação de alta vibração em siderurgia...",
            height=150,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            language = st.selectbox(
                "Idioma:",
                ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"],
                label_visibility="collapsed"
            )
        
        with col2:
            top_k = st.slider(
                "Número de recomendações:",
                min_value=1,
                max_value=20,
                value=10,
                label_visibility="collapsed"
            )
        
        submitted = st.button("🔍 Buscar Recomendações", use_container_width=True)
        
        return user_query if submitted and user_query else None
    
    with tab2:
        st.info("Templates pré-definidos para queries comuns")
        
        templates = {
            "Vibração Alta": "Preciso de um rolamento resistente a vibração alta para aplicação em siderurgia",
            "Operação Contínua": "Rolamento para operação contínua 24/7 em ambiente industrial",
            "Alta Temperatura": "Rolamento que suporte operação em temperaturas acima de 100°C",
            "Baixo Custo": "Rolamento de baixo custo para aplicação de baixa criticidade",
        }
        
        selected_template = st.selectbox("Selecione um template:", list(templates.keys()))
        
        if st.button("Usar Template", use_container_width=True):
            return templates[selected_template]
    
    with tab3:
        st.info("Exemplos de queries bem-sucedidas")
        
        examples = [
            "Rolamento angular para compressor industrial com carga média",
            "Rolamento cilíndrico para transmissão de potência em indústria alimentícia",
            "Rolamento esférico autocompensador para máquinas têxteis",
        ]
        
        for i, example in enumerate(examples, 1):
            if st.button(f"{i}. {example}"):
                return example
    
    return None
