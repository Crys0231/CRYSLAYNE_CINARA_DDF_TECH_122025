"""Renderiza resultados das recomendações"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def render_results(recommendations, products_data):
    """Renderiza resultados das recomendações"""
    
    if not recommendations:
        st.warning("⚠️ Nenhuma recomendação encontrada")
        return
    
    st.success(f"✅ Encontradas {len(recommendations)} recomendações")
    st.divider()

    # Abas de visualização
    tab1, tab2, tab3 = st.tabs(["📊 Ranking", "📈 Comparação", "💾 Exportar"])

    with tab1:
        st.subheader("Top 10 Recomendações")


        results_data = []
        for i, rec in enumerate(recommendations[:10]):
            results_data.append({
                'Rank': i + 1,
                'Produto': rec.get('product_name', 'N/A'),
                'Score': f"{rec.get('score', 0):.1%}",
                'Preço': f"R$ {rec.get('price', 0):,.2f}",
                'Tipo': rec.get('bearing_type', 'N/A'),
            })

        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True, hide_index=True)

        # Detalhes de cada recomendação
        st.subheader("Detalhes das Recomendações")

        for i, rec in enumerate(recommendations[:5], 1):
            with st.expander(
                f"#{i} - {rec.get('product_name', 'N/A')} (Score: {rec.get('score', 0):.1%})"
            ):
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Score", f"{rec.get('score', 0):.1%}")

                with col2:
                    # Preço formatado corretamente
                    st.metric("Preço", f"R$ {rec.get('price', 0):,.0f}")

                with col3:
                    st.metric("Tipo", rec.get('bearing_type', 'N/A'))

                with col4:
                    st.metric("RPM", f"{rec.get('rpm_capacity', 0):,}")

                st.write("**Descrição Técnica:**")
                st.caption(rec.get('technical_description', 'N/A'))

    with tab2:
        st.subheader("Comparação de Produtos")
        top_5 = recommendations[:5]
        
        if len(top_5) > 0:
            products = [rec.get('product_name', 'N/A')[:25] for rec in top_5]
            scores = [rec.get('score', 0) for rec in top_5]
            colors = [
                '#3FB950' if score > 0.4 
                else '#FFA657' if score > 0.3 
                else '#F85149' 
                for score in scores
            ]
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Gráfico horizontal para melhor legibilidade
            bars = ax.barh(products, scores, color=colors, edgecolor='black', linewidth=1.5, height=0.6)
            ax.set_xlabel('Score de Similaridade', fontweight='bold', fontsize=12)
            ax.set_title('Top 5 Melhores Recomendações', fontweight='bold', fontsize=16, pad=20)
            ax.set_xlim(0, 1)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            for i, (score, product) in enumerate(zip(scores, products)):
                ax.text(score + 0.03, i, f'{score:.1%}', va='center', fontweight='bold', fontsize=11)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("Sem dados para exibir gráfico")

    with tab3:
        st.subheader("Exportar Resultados")
        
        # Criar DataFrame para exportação
        export_data = []
        for i, rec in enumerate(recommendations[:10]):
            export_data.append({
                'Rank': i + 1,
                'Produto': rec.get('product_name', 'N/A'),
                'Score': f"{rec.get('score', 0):.1%}",
                'Tipo': rec.get('bearing_type', 'N/A'),
                'Preço': f"R$ {rec.get('price', 0):,.2f}",
                'RPM': rec.get('rpm_capacity', 0),
                'Descrição': rec.get('technical_description', 'N/A')[:100],
            })
        
        export_df = pd.DataFrame(export_data)
        
        # Download CSV
        csv = export_df.to_csv(index=False, encoding='utf-8-sig')
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="recomendacoes_rolamentos.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.info("💡 Abra o arquivo no Excel para análise completa com formatação")
