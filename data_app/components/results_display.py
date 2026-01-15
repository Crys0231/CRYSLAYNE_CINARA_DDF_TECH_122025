import streamlit as st
import pandas as pd

def render_results(recommendations, products_data):
    """Renderiza resultados das recomendações"""
    
    st.success(f"✅ Encontradas {len(recommendations)} recomendações")
    st.divider()
    
    # Abas de visualização
    tab1, tab2, tab3 = st.tabs(["📊 Ranking", "📈 Comparação", "💾 Exportar"])
    
    with tab1:
        st.subheader("Top 10 Recomendações")
        
        # Criar dataframe com recomendações
        results_df = pd.DataFrame([
            {
                'Rank': i + 1,
                'Produto': rec['product_name'],
                'Score': f"{rec['score']:.1%}",
                'Preço': f"R$ {rec['price']:,.2f}",
                'Tipo': rec['bearing_type'],
            }
            for i, rec in enumerate(recommendations[:10])
        ])
        
        st.dataframe(results_df, use_container_width=True)
        
        # Detalhes de cada recomendação
        st.subheader("Detalhes das Recomendações")
        
        for i, rec in enumerate(recommendations[:5], 1):
            with st.expander(f"#{i} - {rec['product_name']} (Score: {rec['score']:.1%})"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Score", f"{rec['score']:.1%}")
                
                with col2:
                    st.metric("Preço", f"R$ {rec['price']:,.0f}")
                
                with col3:
                    st.metric("Tipo", rec['bearing_type'])
                
                with col4:
                    st.metric("RPM", f"{rec['rpm_capacity']:,}")
                
                st.write("**Descrição Técnica:**")
                st.caption(rec['technical_description'])
    
    with tab2:
        st.subheader("Comparação de Produtos")
        
        # Gráfico de comparação
        import matplotlib.pyplot as plt
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        top_5 = recommendations[:5]
        products = [rec['product_name'][:15] for rec in top_5]
        scores = [rec['score'] for rec in top_5]
        
        colors = ['#2ca02c' if score > 0.4 else '#ff7f0e' if score > 0.3 else '#d62728' for score in scores]
        
        ax.barh(products, scores, color=colors, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Score de Similaridade')
        ax.set_title('Comparação dos 5 Melhores Resultados')
        ax.set_xlim(0, 1)
        
        for i, score in enumerate(scores):
            ax.text(score + 0.02, i, f'{score:.1%}', va='center')
        
        st.pyplot(fig)
    
    with tab3:
        st.subheader("Exportar Resultados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download CSV", use_container_width=True):
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Clique para baixar",
                    data=csv,
                    file_name="recomendacoes.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📄 Download PDF", use_container_width=True):
                st.info("Funcionalidade PDF em desenvolvimento...")
