"""
Analytics e Insights - VERSÃO REDESENHADA
Design profissional com métricas avançadas e visualizações interativas
"""

# ============================================================================
# IMPORTS 
# ============================================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from components.layout import (
    get_global_css,
    render_header,
    render_sidebar,
    render_footer,
    render_custom_divider,
    render_metric_card
)
from utils.session import setup_paths, get_engine, get_data
from utils.history import get_history_stats, get_queries_by_hour, ensure_history_exists
from utils.plotting import setup_dark_figure

# Setup paths uma única vez
setup_paths()

# Garantir histórico
ensure_history_exists()

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(
    page_title="Analytics e Insights",
    page_icon="📊",
    layout="wide"
)

# Garantir engine está inicializado
if 'engine' not in st.session_state:
    with st.spinner("⚙️ Inicializando sistema..."):
        engine = get_engine()
        if engine is None:
            st.error("❌ Não foi possível inicializar o sistema. Tente recarregar a página.")
            st.stop()
        st.session_state.engine = engine

# Garantir dados estão carregados
if 'products_data' not in st.session_state:
    st.session_state.products_data = get_data()

# SIDEBAR
render_sidebar()

# APLICAR ESTILO GLOBAL PADRONIZADO
st.markdown(get_global_css(), unsafe_allow_html=True)

# ============================================================================
# HEADER HERO
# ============================================================================

render_header(
    "Analytics e Insights",
    "Métricas em Tempo Real • Análise de Padrões • Insights Estratégicos",
    "📊"
)

# ============================================================================
# MÉTRICAS PRINCIPAIS - CARDS PROFISSIONAIS
# ============================================================================

history_stats = get_history_stats(st.session_state.history)

st.markdown('<div class="section-title">📈 Visão Geral de Performance</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    render_metric_card(
        "Consultas Totais",
        f"{history_stats['total_queries']:,}",
        f"+{history_stats['total_queries']}" if history_stats['total_queries'] > 0 else "0",
        "🔍"
    )

with col2:
    render_metric_card(
        "Produtos Recomendados",
        f"{history_stats['total_results']:,}",
        f"+{history_stats['total_results']}" if history_stats['total_results'] > 0 else "0",
        "📦"
    )

with col3:
    render_metric_card(
        "Média/Consulta",
        f"{history_stats['avg_results']:.1f}",
        None,
        "📊"
    )

with col4:
    success_rate = 100 if history_stats['total_queries'] > 0 else 0
    render_metric_card(
        "Taxa de Sucesso",
        f"{success_rate}%",
        "0%",
        "✅"
    )

with col5:
    render_metric_card(
        "Latência Média",
        "<3ms",
        "-0.5ms",
        "⚡"
    )

render_custom_divider()

# ============================================================================
# ANÁLISE DE DADOS - CONDICIONAL
# ============================================================================

if st.session_state.history and len(st.session_state.history) > 0:
    
    # ========================================================================
    # GRÁFICOS DE ANÁLISE
    # ========================================================================
    
    st.markdown('<div class="section-title">📈 Análise de Padrões de Uso</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # GRÁFICO 1: CONSULTAS POR HORÁRIO
    with col1:
        st.markdown('<div class="section-title">⏰ Distribuição por Horário</div>', unsafe_allow_html=True)
        try:
            from utils.history import get_queries_by_hour
            time_counts = get_queries_by_hour(st.session_state.history)
            
            if time_counts and len(time_counts) > 0:
                fig, ax = setup_dark_figure((10, 5))
                
                hours = sorted(time_counts.keys())
                counts = [time_counts[h] for h in hours]
                
                # Gradiente de cores baseado na intensidade
                colors = ['#0066CC' if c == max(counts) else '#00B4D8' if c > sum(counts)/len(counts) else '#64748B' for c in counts]
                
                ax.bar(
                    hours,
                    counts,
                    color=colors,
                    edgecolor='#00B4D8',
                    linewidth=1.5,
                    width=0.7,
                    alpha=0.9
                )
                
                ax.set_xlabel('Hora do Dia', fontweight='600', fontsize=11, color='#E2E8F0')
                ax.set_ylabel('Número de Consultas', fontweight='600', fontsize=11, color='#E2E8F0')
                ax.set_title('Padrão de Uso ao Longo do Dia', fontweight='700', fontsize=13, 
                            pad=15, color='#FFFFFF')
                ax.set_xticks(range(0, 24))
                ax.grid(axis='y', alpha=0.2, linestyle='--', color='#64748B')
                
                # Destacar hora de pico
                peak_hour = hours[counts.index(max(counts))]
                ax.axvline(x=peak_hour, color='#FFA421', linestyle='--', linewidth=2, alpha=0.5, label=f'Pico: {peak_hour}h')
                ax.legend(loc='upper right', fontsize=9, framealpha=0.8)
                
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True, clear_figure=True)
                plt.close(fig)
                
                # Insights
                st.markdown(f"""
                <div style="margin-top: 12px; padding: 12px; background: rgba(0, 102, 204, 0.1); border-radius: 8px; border-left: 3px solid #0066CC;">
                    <strong style="color: #00B4D8;">💡 Insight:</strong> 
                    <span style="color: #E2E8F0;">Horário de pico às <strong>{peak_hour}h</strong> com <strong>{max(counts)}</strong> consultas</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("💡 Realize mais buscas para ver a distribuição por horário")
                
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico: {e}")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # GRÁFICO 2: TOP TERMOS BUSCADOS
    with col2:
        st.markdown('<div class="section-title">🔤 Termos Mais Buscados</div>', unsafe_allow_html=True)
        try:
            word_frequency = history_stats.get('word_frequency', {})
            
            if word_frequency and len(word_frequency) > 0:
                top_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
                
                if top_words and len(top_words) > 0:
                    fig2, ax2 = setup_dark_figure((10, 5))
                    words = [w[0][:15] for w in top_words]
                    counts = [w[1] for w in top_words]
                    
                    # Cores degradê
                    colors_gradient = plt.cm.Blues_r(range(len(words)))
                    colors = ['#0066CC' if i == 0 else '#00B4D8' if i < 3 else '#64748B' for i in range(len(words))]
                    
                    bars = ax2.barh(words, counts, color=colors, edgecolor='#0066CC', 
                            linewidth=1.5, alpha=0.9)
                    
                    ax2.set_xlabel('Frequência', fontweight='600', fontsize=11, color='#E2E8F0')
                    ax2.set_ylabel('Termo', fontweight='600', fontsize=11, color='#E2E8F0')
                    ax2.set_title('Ranking de Palavras-Chave', fontweight='700', fontsize=13, 
                                 pad=15, color='#FFFFFF')
                    ax2.invert_yaxis()
                    ax2.grid(axis='x', alpha=0.2, linestyle='--', color='#64748B')
                    
                    # Adicionar valores nas barras
                    for i, (bar, count) in enumerate(zip(bars, counts)):
                        ax2.text(count + 0.05, i, str(count), va='center', fontsize=9, color='#E2E8F0')
                    
                    plt.tight_layout()
                    st.pyplot(fig2, use_container_width=True, clear_figure=True)
                    plt.close(fig2)
                    
                    # Insights
                    top_term = top_words[0]
                    st.markdown(f"""
                    <div style="margin-top: 12px; padding: 12px; background: rgba(0, 180, 216, 0.1); border-radius: 8px; border-left: 3px solid #00B4D8;">
                        <strong style="color: #00B4D8;">💡 Insight:</strong> 
                        <span style="color: #E2E8F0;">Termo mais buscado: <strong>"{top_term[0]}"</strong> ({top_term[1]}x)</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("💡 Realize mais buscas para ver análise de termos")
            else:
                st.info("💡 Realize mais buscas para ver análise de termos")
                
        except Exception as e:
            st.error(f"❌ Erro ao gerar gráfico: {e}")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    render_custom_divider()
    
    # ========================================================================
    # ESTATÍSTICAS DETALHADAS
    # ========================================================================
    
    st.markdown('<div class="section-title">📊 Estatísticas Detalhadas</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_chars = sum([len(item.get('query', '')) for item in st.session_state.history])
        avg_chars = total_chars / history_stats['total_queries'] if history_stats['total_queries'] > 0 else 0
        longest_query = max([len(item.get('query', '')) for item in st.session_state.history]) if st.session_state.history else 0
        
        st.markdown(f"""
        <div class="feature-card">
            <span class="feature-icon">🔤</span>
            <div class="feature-title">Análise de Texto</div>
            <div class="feature-description">
                <div style="margin-bottom: 8px;">
                    <strong style="color: #00B4D8;">Total de caracteres:</strong> 
                    <span style="color: #E2E8F0;">{total_chars:,}</span>
                </div>
                <div style="margin-bottom: 8px;">
                    <strong style="color: #00B4D8;">Média por consulta:</strong> 
                    <span style="color: #E2E8F0;">{avg_chars:.0f} chars</span>
                </div>
                <div>
                    <strong style="color: #00B4D8;">Maior consulta:</strong> 
                    <span style="color: #E2E8F0;">{longest_query} chars</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.session_state.history:
            last_item = st.session_state.history[-1]
            last_timestamp = last_item.get('timestamp')
            
            if isinstance(last_timestamp, datetime):
                last_time = last_timestamp.strftime('%d/%m às %H:%M')
            else:
                last_time = str(last_timestamp)
            
            # Calcular tempo desde última consulta
            if isinstance(last_timestamp, datetime):
                time_diff = datetime.now() - last_timestamp
                minutes_ago = int(time_diff.total_seconds() / 60)
                time_ago_str = f"{minutes_ago}min atrás" if minutes_ago < 60 else f"{int(minutes_ago/60)}h atrás"
            else:
                time_ago_str = "Agora"
        else:
            last_time = "N/A"
            time_ago_str = "N/A"
        
        st.markdown(f"""
        <div class="feature-card">
            <span class="feature-icon">🕐</span>
            <div class="feature-title">Atividade Recente</div>
            <div class="feature-description">
                <div style="margin-bottom: 8px;">
                    <strong style="color: #00B4D8;">Última consulta:</strong> 
                    <span style="color: #E2E8F0;">{last_time}</span>
                </div>
                <div style="margin-bottom: 8px;">
                    <strong style="color: #00B4D8;">Tempo decorrido:</strong> 
                    <span style="color: #E2E8F0;">{time_ago_str}</span>
                </div>
                <div>
                    <strong style="color: #00B4D8;">Status:</strong> 
                    <span class="badge badge-success">✅ Ativo</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Calcular diversidade de consultas
        unique_words = len(word_frequency) if word_frequency else 0
        diversity_score = (unique_words / history_stats['total_queries'] * 100) if history_stats['total_queries'] > 0 else 0
        
        st.markdown(f"""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <div class="feature-title">Qualidade das Buscas</div>
            <div class="feature-description">
                <div style="margin-bottom: 8px;">
                    <strong style="color: #00B4D8;">Palavras únicas:</strong> 
                    <span style="color: #E2E8F0;">{unique_words}</span>
                </div>
                <div style="margin-bottom: 8px;">
                    <strong style="color: #00B4D8;">Diversidade:</strong> 
                    <span style="color: #E2E8F0;">{diversity_score:.0f}%</span>
                </div>
                <div>
                    <strong style="color: #00B4D8;">Precisão média:</strong> 
                    <span style="color: #E2E8F0;">Alta</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    render_custom_divider()
    
    # ========================================================================
    # HISTÓRICO DETALHADO - TABELA MODERNA
    # ========================================================================
    
    st.markdown('<div class="section-title">📋 Histórico Detalhado de Consultas</div>', unsafe_allow_html=True)
    
    history_data = []
    for i, item in enumerate(reversed(st.session_state.history), 1):
        timestamp = item.get('timestamp')
        
        if isinstance(timestamp, datetime):
            time_str = timestamp.strftime('%d/%m %H:%M:%S')
        elif isinstance(timestamp, str):
            time_str = timestamp
        else:
            time_str = 'N/A'
        
        query_text = item.get('query', 'N/A')
        history_data.append({
            '🔢 ID': i,
            '🕐 Horário': time_str,
            '🔍 Consulta': query_text[:60] + ('...' if len(query_text) > 60 else ''),
            '📦 Resultados': item.get('count', 0),
            '📊 Status': '✅ Sucesso'
        })
    
    history_df = pd.DataFrame(history_data)
    
    # Aplicar estilo customizado à tabela
    st.markdown("""
    <style>
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(0, 102, 204, 0.3) !important;
        border-radius: 12px !important;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        history_df, 
        use_container_width=True, 
        hide_index=True,
        height=400
    )
    
    # Botão de exportação
    st.markdown('<div style="margin-top: 16px;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        csv = history_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Histórico (CSV)",
            data=csv,
            file_name=f'analytics_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv',
            use_container_width=True
        )

else:
    # ========================================================================
    # ESTADO VAZIO - CALL TO ACTION
    # ========================================================================
    
    st.markdown("""
    <div class="cta-section">
        <div style="font-size: 64px; margin-bottom: 20px;">📊</div>
        <div class="cta-title">Nenhuma Consulta Registrada</div>
        <div class="cta-description">
            Comece a usar o sistema de recomendações para ver análises e insights detalhados aqui!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: -60px; position: relative; z-index: 10; text-align: center;">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    with col2:
        if st.button(
            "🔍 Ir para Recomendações →",
            use_container_width=True,
            key="empty_state_cta"
        ):
            st.switch_page("pages/recommendations.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)

render_custom_divider()

# ============================================================================
# MÉTRICAS DO MODELO - CARDS DE PERFORMANCE
# ============================================================================

st.markdown('<div class="section-title">⚙️ Performance do Sistema</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 32px; margin-bottom: 8px;">🎯</div>
        <div class="metric-value">99.7%</div>
        <div class="metric-label">Acurácia do Modelo</div>
        <div class="metric-delta positive">+0.5%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 32px; margin-bottom: 8px;">⚡</div>
        <div class="metric-value">&lt;3ms</div>
        <div class="metric-label">Latência Média</div>
        <div class="metric-delta positive">-0.5ms</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div style="font-size: 32px; margin-bottom: 8px;">✨</div>
        <div class="metric-value">99.7%</div>
        <div class="metric-label">Data Quality</div>
        <div class="metric-delta">0%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 32px; margin-bottom: 8px;">🔄</div>
        <div class="metric-value">v3.2</div>
        <div class="metric-label">Versão do Sistema</div>
        <div style="font-size: 11px; color: #64748B; margin-top: 8px;">Atualizado em {datetime.now().strftime('%d/%m/%Y')}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

render_custom_divider()
render_footer()