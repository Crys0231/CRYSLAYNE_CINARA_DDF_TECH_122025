"""
Página de recomendações
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from src.recommendation_engine import RecommendationEngine
    from data_app.utils.data_loader import load_products_data
    from data_app.utils.formatters import (
        format_price, format_score, format_bearing_type, format_industry
    )
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")

def render_recommendations():
    """Renderiza página de recomendações"""
    
    st.title("🔍 Recomendações de Rolamentos")
    
    # Inicializar engines
    if 'recommendation_engine' not in st.session_state:
        try:
            st.session_state.recommendation_engine = RecommendationEngine()
            st.session_state.products_data = load_products_data()
            st.session_state.history = []
        except Exception as e:
            st.error(f"❌ Erro ao inicializar: {e}")
            return
    
    # Input
    st.subheader("📝 Descreva seu problema")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_query = st.text_area(
            "Descrição do problema:",
            placeholder="Ex: Preciso de um rolamento para aplicação de alta vibração em siderurgia com operação contínua...",
            height=120,
            label_visibility="collapsed"
        )
    
    with col2:
        st.caption("Idioma")
        language = st.selectbox(
            "Selecione:",
            ["🇧🇷 Português", "🇺🇸 English", "🇪🇸 Español"],
            label_visibility="collapsed"
        )
        
        st.caption("Resultados")
        top_k = st.slider(
            "Mostrar:",
            min_value=1,
            max_value=20,
            value=10,
            label_visibility="collapsed"
        )
    
    # Botão de busca
    if st.button("🔍 Buscar Recomendações", use_container_width=True, key="search_btn"):
        if not user_query:
            st.warning("⚠️ Digite uma descrição de problema!")
        else:
            with st.spinner("🔄 Analisando e gerando recomendações..."):
                try:
                    # Obter recomendações
                    recommendations = st.session_state.recommendation_engine.recommend(
                        user_query,
                        top_k=top_k
                    )
                    
                    # Adicionar ao histórico
                    st.session_state.history.append({
                        'query': user_query,
                        'count': len(recommendations)
                    })
                    
                    # Exibir resultados
                    st.success(f"✅ {len(recommendations)} recomendações encontradas!")
                    
                    # Abas
                    tab1, tab2, tab3 = st.tabs(["📊 Ranking", "📈 Gráfico", "💾 Exportar"])
                    
                    with tab1:
                        st.subheader("Top Recomendações")
                        
                        # Dataframe
                        results_data = []
                        for i, rec in enumerate(recommendations, 1):
                            results_data.append({
                                'Rank': i,
                                'Produto': rec.get('product_name', 'N/A'),
                                'Score': f"{rec.get('score', 0):.1%}",
                                'Tipo': format_bearing_type(rec.get('bearing_type', 'N/A')),
                                'Preço': format_price(rec.get('price', 0)),
                            })
                        
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, use_container_width=True, hide_index=True)
                        
                        # Detalhes
                        st.subheader("Detalhes dos Produtos")
                        
                        for i, rec in enumerate(recommendations[:5], 1):
                            with st.expander(
                                f"#{i} - {rec.get('product_name', 'N/A')} | Score: {rec.get('score', 0):.1%}"
                            ):
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("Score", f"{rec.get('score', 0):.1%}")
                                
                                with col2:
                                    st.metric("Preço", format_price(rec.get('price', 0)).split())
                                
                                with col3:
                                    st.metric("RPM", f"{rec.get('rpm_capacity', 0):,}")
                                
                                with col4:
                                    st.metric("Tipo", rec.get('bearing_type', 'N/A'))
                                
                                st.write("**Descrição Técnica:**")
                                st.caption(rec.get('technical_description', 'N/A'))
                    
                    with tab2:
                        st.subheader("Comparação de Scores")
                        
                        import matplotlib.pyplot as plt
                        
                        fig, ax = plt.subplots(figsize=(12, 6))
                        
                        top_n = recommendations[:5]
                        names = [rec.get('product_name', 'N/A')[:20] for rec in top_n]
                        scores = [rec.get('score', 0) for rec in top_n]
                        
                        colors = ['#2ca02c' if s > 0.4 else '#ff7f0e' if s > 0.3 else '#d62728' for s in scores]
                        
                        ax.barh(names, scores, color=colors, edgecolor='black', linewidth=1.5)
                        ax.set_xlabel('Score de Similaridade', fontweight='bold')
                        ax.set_title('Top 5 Recomendações', fontweight='bold', fontsize=14)
                        ax.set_xlim(0, 1)
                        
                        for j, score in enumerate(scores):
                            ax.text(score + 0.02, j, f'{score:.1%}', va='center', fontweight='bold')
                        
                        st.pyplot(fig)
                    
                    with tab3:
                        st.subheader("Exportar Resultados")
                        
                        # CSV
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name="recomendacoes.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        st.info("💡 Dica: Use o arquivo CSV para análise em Excel ou integração com sistemas")
                
                except Exception as e:
                    st.error(f"❌ Erro ao processar: {str(e)}")
    
    # Histórico
    if st.session_state.history:
        st.divider()
        st.subheader("📋 Histórico Recente")
        
        for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.caption(f"{i}. {item['query'][:60]}... ({item['count']} resultados)")

# Renderizar se executado diretamente
if __name__ == "__main__":
    render_recommendations()
