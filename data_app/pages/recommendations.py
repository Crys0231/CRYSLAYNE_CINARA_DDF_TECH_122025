"""
Página de recomendações com dados REAIS do histórico
"""
# ============================================================================
# IMPORTS
# ============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import streamlit as st
import time  # IMPORTANTE: para medir processing_time

from data_app.utils.logger import setup_recommendations_logger
from data_app.utils.session import setup_paths, get_engine, get_data
from data_app.utils.history import ensure_history_exists
from data_app.utils.examples import load_examples

try:
    from data_app.components.layout import (
        get_global_css, 
        render_sidebar,
        render_header, 
        render_footer
    )
except ImportError as e:
    st.warning(f"⚠️ Alguns módulos não foram importados: {e}")

# Setup paths uma única vez
setup_paths()

# Garantir histórico
ensure_history_exists()

# ============================================================================
# IMPORTAR MONITORAMENTO
# ============================================================================
try:
    from monitoring import StreamlitMonitor
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False
    st.warning("⚠️ Sistema de monitoramento não disponível")


# ============================================================================
# CONFIGURAÇÃO
# ============================================================================


# LOGGER
logger = setup_recommendations_logger()
logger.info("=" * 60)
logger.info("🔍 Página de recomendações carregada")
logger.info("=" * 60)

st.set_page_config(
    page_title="Recomendações",
    page_icon="🔍",
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

# ============================================================================
# INICIALIZAR MONITORAMENTO
# ============================================================================

if MONITORING_AVAILABLE and 'monitor' not in st.session_state:
    try:
        st.session_state.monitor = StreamlitMonitor(
            session_state=st.session_state
        )
        
        # Configurar baseline do modelo
        baseline_status = st.session_state.monitor.initialize_baseline()
        
        logger.info("Monitor inicializado")
        logger.info(f"Baseline: {baseline_status['samples']} amostras")
        logger.info(f"Média: {baseline_status['mean']:.3f}")
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar monitor: {e}")
        st.session_state.monitor = None

# Alias para uso mais fácil
monitor = st.session_state.get('monitor')

# SIDEBAR
render_sidebar()

# APLICAR ESTILO GLOBAL PADRONIZADO
st.markdown(get_global_css(), unsafe_allow_html=True)

# ============================================================================
# CARREGAR EXEMPLOS
# ============================================================================

@st.cache_data
def get_examples():
    """Carrega exemplos com cache para performance"""
    try:
        examples = load_examples()
        # LOGGING
        logger.info(f"✅ {len(examples)} categorias de exemplos carregadas")
        return examples
    except FileNotFoundError as e:
        # LOGGING DE ERRO
        logger.error(f"❌ Arquivo de exemplos não encontrado: {e}", exc_info=True)
        st.error(str(e))
        return {}
    except Exception as e:
        # LOGGING DE ERRO
        logger.error(f"❌ Erro ao carregar exemplos: {e}", exc_info=True)
        st.error(f"❌ Erro ao carregar exemplos: {e}")
        return {}

EXAMPLES_BY_INDUSTRY = get_examples()

# ============================================================================
# CSS ESPECÍFICO DA PÁGINA
# ============================================================================

# APLICAR ESTILO GLOBAL
st.markdown(get_global_css(), unsafe_allow_html=True)

# CSS adicional específico para product cards
st.markdown("""
<style>
    .product-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 250ms ease-in-out;
        backdrop-filter: blur(10px);
    }
    
    .product-card:hover {
        background: rgba(0, 102, 204, 0.1);
        border-color: rgba(0, 102, 204, 0.4);
        box-shadow: 0 8px 24px rgba(0, 102, 204, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-badge {
        display: inline-block;
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .score-high {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    }
    
    .score-medium {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
    }
    
    .score-low {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
    }
</style>
""", unsafe_allow_html=True)
# ============================================================================
# HEADER
# ============================================================================

render_header("🔍 Recomendações Personalizadas", "Encontre o rolamento ideal para sua aplicação")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# SEÇÃO DE ENTRADA
# ============================================================================

st.markdown("### 🔍 Descreva Seu Problema")

col1, col2 = st.columns([3, 1])

# Inicializar
if 'user_query_value' not in st.session_state:
    st.session_state.user_query_value = ""


with col1:
    user_query = st.text_area(
        "Problema Técnico:",
        value=st.session_state.user_query_value,
        placeholder="Ex: Preciso de um rolamento para máquina de alta vibração em siderurgia, com RPM acima de 10000 e carga média...",
        height=120,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**⚙️ Configurações**")
    top_k = st.slider(
        "Resultados:",
        min_value=5,
        max_value=20,
        value=10,
        step=1
    )
# Botão de busca
search_col1, search_col2, search_col3 = st.columns([1, 1, 2])

with search_col1:
    search_btn = st.button(
        "🔍 Buscar Recomendações",
        use_container_width=True,
        key="search_recommendations"
    )

with search_col3:
    st.caption("💡 Quanto mais detalhado sua descrição, melhores os resultados!")


# ============================================================================
# PROCESSAMENTO DE BUSCA (LINHA ~240)
# ============================================================================

if search_btn:
    if not user_query or user_query.strip() == "":
        st.warning("⚠️ Por favor, descreva seu problema técnico!")
    else:
        with st.spinner("🔄 Analisando..."):
            try:
                # INÍCIO DO MONITORAMENTO
                import time
                start_time = time.time()
                
                # Gerar recomendações
                recommendations = st.session_state.engine.recommend(
                    user_query, 
                    top_k=int(top_k)
                )
                
                # FIM DO MONITORAMENTO
                processing_time = time.time() - start_time
                
                # MONITORAMENTO AUTOMÁTICO
                monitoring_status = None
                if monitor:
                    try:
                        monitoring_status = monitor.track_recommendation(
                            query=user_query,
                            recommendations=recommendations,
                            processing_time=processing_time,
                            user_id="anonymous"
                        )
                        
                        logger.info(
                            f"Monitoramento: {monitoring_status['num_results']} resultados, "
                            f"{monitoring_status['processing_time_ms']:.1f}ms, "
                            f"Score: {monitoring_status['top_score']:.1%}"
                        )
                        
                    except Exception as e:
                        logger.error(f"❌ Erro no monitoramento: {e}")
                
                if not recommendations:
                    logger.warning(f"⚠️ Nenhuma recomendação encontrada para: {user_query[:50]}...")
                    st.warning("⚠️ Nenhuma recomendação encontrada para sua descrição.")
                else:
                    ensure_history_exists()
                    
                    # Criar item do histórico
                    history_item = {
                        'query': user_query,
                        'count': len(recommendations),
                        'timestamp': datetime.now()
                    }
                    
                    # Adicionar ao histórico
                    st.session_state.history.append(history_item)
                    
                    # LOGGING
                    logger.info(
                        f"✅ Recomendações geradas: {len(recommendations)} resultados "
                        f"em {processing_time*1000:.2f}ms para query: {user_query[:50]}..."
                    )
                    
                    # VERIFICAR ALERTAS E DRIFT
                    alert_messages = []
                    
                    if monitoring_status:
                        if monitoring_status.get('drift_detected'):
                            alert_messages.append({
                                'type': 'warning',
                                'message': f"⚠️ **Drift detectado!** Score atual: {monitoring_status['top_score']:.1%}"
                            })
                            alert_messages.append({
                                'type': 'info',
                                'message': "Considere retreinar o modelo com dados recentes"
                            })
                        
                        if monitoring_status.get('active_alerts', 0) > 0:
                            alert_messages.append({
                                'type': 'error',
                                'message': f"🚨 {monitoring_status['active_alerts']} alertas ativos - Verifique o dashboard de monitoramento"
                            })
                    
                    # Mensagem de sucesso com info de performance
                    success_msg = f"{len(recommendations)} recomendações encontradas"
                    if monitoring_status:
                        success_msg += f" em {monitoring_status['processing_time_ms']:.1f}ms!"
                    else:
                        success_msg += f" em {processing_time*1000:.1f}ms!"
                    
                    st.success(success_msg)
                    
                    # Mostrar alertas se houver
                    for alert in alert_messages:
                        if alert['type'] == 'warning':
                            st.warning(alert['message'])
                        elif alert['type'] == 'error':
                            st.error(alert['message'])
                        elif alert['type'] == 'info':
                            st.info(alert['message'])
                        
                    # ============================================================
                    # ABAS DE RESULTADOS
                    # ============================================================
                    
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "📊 Ranking",
                        "📈 Gráfico",
                        "🎯 Comparação",
                        "💾 Exportar",
                        "📋 Detalhes"
                    ])
                    
                    # ================== TAB 1: RANKING ==================
                    with tab1:
                        st.subheader("🏆 Top Recomendações")
                        
                        # Criar DataFrame com estilo
                        results_data = []
                        for i, rec in enumerate(recommendations, 1):
                            results_data.append({
                                '🏅': f"#{i}",
                                'Produto': rec.get('product_name', 'N/A'),
                                'Score': f"⭐ {rec.get('score', 0):.1%}",
                                'Tipo': rec.get('bearing_type', 'N/A'),
                                'Preço': f"💰 R$ {rec.get('price', 0):,.2f}",
                                'RPM': f"⚡ {rec.get('rpm_capacity', 0):,}",
                            })
                        
                        results_df = pd.DataFrame(results_data)
                        
                        st.dataframe(
                            results_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                '🏅': st.column_config.TextColumn(width="small"),
                                'Produto': st.column_config.TextColumn(width="large"),
                                'Score': st.column_config.TextColumn(width="small"),
                                'Tipo': st.column_config.TextColumn(width="medium"),
                                'Preço': st.column_config.TextColumn(width="medium"),
                                'RPM': st.column_config.TextColumn(width="small"),
                            }
                        )
                    
                    # ================== TAB 2: GRÁFICO ==================
                    with tab2:
                        st.subheader("📊 Análise Visual das Recomendações")
                        
                        top_5 = recommendations[:5]
                        
                        if len(top_5) > 0:
                            # Preparar dados
                            names = [f"#{i+1} {rec.get('product_name', 'N/A')[:25]}" + ('...' if len(rec.get('product_name', '')) > 25 else '') 
                                    for i, rec in enumerate(top_5)]
                            scores = [rec.get('score', 0) * 100 for rec in top_5]  # Converter para porcentagem
                            prices = [rec.get('price', 0) for rec in top_5]
                            rpm_values = [rec.get('rpm_capacity', 0) for rec in top_5]
                            
                            # Criar figura com múltiplos gráficos
                            fig = plt.figure(figsize=(14, 8))
                            fig.patch.set_facecolor('#0F172A')
                            gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
                            
                            # === GRÁFICO 1: Score de Similaridade (Barras Horizontais) ===
                            ax1 = fig.add_subplot(gs[0, :])
                            ax1.set_facecolor('#1A1F3A')
                            
                            # Cores baseadas no score
                            colors = []
                            for score in scores:
                                if score >= 70:
                                    colors.append('#10B981')  # Verde - Excelente
                                elif score >= 50:
                                    colors.append('#F59E0B')  # Amarelo - Bom
                                else:
                                    colors.append('#EF4444')  # Vermelho - Regular
                            
                            bars = ax1.barh(range(len(names)), scores, color=colors, edgecolor='#E2E8F0', 
                                           linewidth=1.5, height=0.7, alpha=0.9)
                            
                            ax1.set_yticks(range(len(names)))
                            ax1.set_yticklabels(names, color='#E2E8F0', fontsize=10)
                            ax1.set_xlabel('Score de Similaridade (%)', fontweight='bold', fontsize=11, color='#E2E8F0')
                            ax1.set_title('🎯 Score de Similaridade com a Requisição', fontweight='bold', 
                                         fontsize=13, pad=15, color='#FFFFFF')
                            ax1.set_xlim(0, 100)
                            ax1.grid(axis='x', alpha=0.2, linestyle='--', color='#64748B')
                            ax1.tick_params(colors='#E2E8F0')
                            
                            # Adicionar valores nas barras
                            for i, (bar, score) in enumerate(zip(bars, scores)):
                                ax1.text(score + 1, i, f'{score:.1f}%', va='center', 
                                        fontweight='bold', fontsize=9, color='#FFFFFF')
                            
                            for spine in ax1.spines.values():
                                spine.set_color('#64748B')
                                spine.set_linewidth(0.5)
                            
                            # === GRÁFICO 2: Preço vs Score (Scatter Plot) ===
                            ax2 = fig.add_subplot(gs[1, 0])
                            ax2.set_facecolor('#1A1F3A')
                            
                            # Scatter plot: Score (x) vs Preço (y)
                            scatter = ax2.scatter(scores, prices, s=[s*20 for s in scores], 
                                                 c=colors, alpha=0.6, edgecolors='#E2E8F0', 
                                                 linewidths=1.5)
                            
                            # Adicionar labels para os 3 melhores
                            for i in range(min(3, len(top_5))):
                                ax2.annotate(f"#{i+1}", 
                                           (scores[i], prices[i]),
                                           xytext=(5, 5), textcoords='offset points',
                                           fontsize=9, fontweight='bold',
                                           color='#FFFFFF',
                                           bbox=dict(boxstyle='round,pad=0.3', 
                                                    facecolor=(0, 102/255, 204/255, 0.7), 
                                                    edgecolor='none'))
                            
                            ax2.set_xlabel('Score (%)', fontweight='bold', fontsize=10, color='#E2E8F0')
                            ax2.set_ylabel('Preço (R$)', fontweight='bold', fontsize=10, color='#E2E8F0')
                            ax2.set_title('💰 Relação Preço × Score', fontweight='bold', 
                                         fontsize=11, pad=10, color='#FFFFFF')
                            ax2.grid(alpha=0.2, linestyle='--', color='#64748B')
                            ax2.tick_params(colors='#E2E8F0')
                            
                            for spine in ax2.spines.values():
                                spine.set_color('#64748B')
                                spine.set_linewidth(0.5)
                            
                            # === GRÁFICO 3: Comparação Multidimensional ===
                            ax3 = fig.add_subplot(gs[1, 1])
                            ax3.set_facecolor('#1A1F3A')
                            
                            # Normalizar valores para comparação (0-100)
                            max_price = max(prices) if prices else 1
                            max_rpm = max(rpm_values) if rpm_values else 1
                            
                            normalized_prices = [(p/max_price)*100 for p in prices]
                            normalized_rpm = [(r/max_rpm)*100 for r in rpm_values]
                            top_scores = scores
                            
                            x = np.arange(len(top_5))
                            width = 0.25
                            
                            bars1 = ax3.bar(x - width, top_scores, width, label='Score (%)', 
                                           color='#0066CC', alpha=0.8, edgecolor='#E2E8F0')
                            bars2 = ax3.bar(x, normalized_prices, width, label='Preço (norm.)', 
                                           color='#00B4D8', alpha=0.8, edgecolor='#E2E8F0')
                            bars3 = ax3.bar(x + width, normalized_rpm, width, label='RPM (norm.)', 
                                           color='#10B981', alpha=0.8, edgecolor='#E2E8F0')
                            
                            ax3.set_xlabel('Top 5 Produtos', fontweight='bold', fontsize=10, color='#E2E8F0')
                            ax3.set_ylabel('Valor Normalizado (%)', fontweight='bold', fontsize=10, color='#E2E8F0')
                            ax3.set_title('⚖️ Comparação Multidimensional', fontweight='bold', 
                                         fontsize=11, pad=10, color='#FFFFFF')
                            ax3.set_xticks(x)
                            ax3.set_xticklabels([f"#{i+1}" for i in range(len(top_5))], 
                                               color='#E2E8F0')
                            ax3.set_ylim(0, 105)
                            ax3.legend(loc='upper right', fontsize=8, 
                                      facecolor=(26/255, 31/255, 58/255, 0.8), 
                                      edgecolor='#64748B',
                                      labelcolor='#E2E8F0')
                            ax3.grid(axis='y', alpha=0.2, linestyle='--', color='#64748B')
                            ax3.tick_params(colors='#E2E8F0')
                            
                            for spine in ax3.spines.values():
                                spine.set_color('#64748B')
                                spine.set_linewidth(0.5)
                            
                            plt.tight_layout()
                            st.pyplot(fig, use_container_width=True)
                            
                            # Informação adicional
                            st.markdown("""
                            <div style="
                                background: var(--card-bg);
                                border: 1px solid var(--border-color);
                                border-radius: 8px;
                                padding: 1rem;
                                margin-top: 1rem;
                                backdrop-filter: blur(10px);
                            ">
                                <div style="color: var(--text-secondary); font-size: 0.9rem; font-family: 'Inter', sans-serif;">
                                    <strong style="color: var(--text-primary);">💡 Como interpretar:</strong><br>
                                    • <strong style="color: #10B981;">Score:</strong> Quanto maior, mais alinhado com sua requisição<br>
                                    • <strong style="color: #00B4D8;">Preço vs Score:</strong> Produtos no canto superior direito oferecem melhor custo-benefício<br>
                                    • <strong style="color: #0066CC;">Comparação:</strong> Visualize o equilíbrio entre score, preço e capacidade RPM
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # ================== TAB 3: COMPARAÇÃO ==================
                    with tab3:
                        st.subheader("⚖️ Análise Comparativa")
                        
                        top_3 = recommendations[:3]
                        
                        if len(top_3) > 0:
                            # Criar colunas dinamicamente baseado no número de itens
                            cols = st.columns(len(top_3))
                            
                            for idx, (col, rec) in enumerate(zip(cols, top_3)):
                                with col:
                                    st.markdown(f"""
                                    <div class="product-card">
                                    <h3 style="color: #FFFFFF; margin: 0 0 12px 0;">#{idx+1}</h3>
                                    <p style="color: #E2E8F0; font-weight: 600; margin: 8px 0;">
                                        {rec.get('product_name', 'N/A')}
                                    </p>
                                    <div style="margin: 12px 0;">
                                        <span class="metric-badge score-high">
                                            ⭐ {rec.get('score', 0):.1%}
                                        </span>
                                    </div>
                                    <hr style="margin: 12px 0; opacity: 0.3;">
                                    <div style="color: #94A3B8; font-size: 13px;">
                                        <p style="margin: 6px 0;"><strong>Tipo:</strong> {rec.get('bearing_type', 'N/A')}</p>
                                        <p style="margin: 6px 0;"><strong>Preço:</strong> R$ {rec.get('price', 0):,.2f}</p>
                                        <p style="margin: 6px 0;"><strong>RPM:</strong> {rec.get('rpm_capacity', 0):,}</p>
                                    </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("⚠️ Não há recomendações suficientes para comparação.")
                    
                    # ================== TAB 4: EXPORTAR ==================
                    with tab4:
                        st.subheader("📥 Exportar Resultados")
                        
                        export_data = []
                        for i, rec in enumerate(recommendations, 1):
                            export_data.append({
                                'Rank': i,
                                'Produto': rec.get('product_name', 'N/A'),
                                'Score': f"{rec.get('score', 0):.1%}",
                                'Tipo': rec.get('bearing_type', 'N/A'),
                                'Preço (R$)': f"{rec.get('price', 0):,.2f}",
                                'RPM': rec.get('rpm_capacity', 0),
                                'Descrição': rec.get('technical_description', '')[:40] if rec.get('technical_description') else 'N/A',
                            })
                        
                        export_df = pd.DataFrame(export_data)
                        csv = export_df.to_csv(index=False, encoding='utf-8-sig')
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv,
                                file_name=f"recomendacoes_{datetime.now().strftime('%d%m%Y_%H%M')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                        
                        with col2:
                            st.info("💡 Importe em Excel para análise adicional")
                        
                        st.dataframe(export_df, use_container_width=True, hide_index=True)
                    
                    # ================== TAB 5: DETALHES ==================
                    with tab5:
                        st.subheader("🔎 Informações Técnicas Detalhadas")
                        
                        for i, rec in enumerate(recommendations[:8], 1):
                            product_name = rec.get('product_name', 'N/A')
                            score = rec.get('score', 0)
                            with st.expander(
                                f"#{i} – {product_name} | Score: {score:.1%}",
                                expanded=(i == 1)
                            ):
                                # Métricas
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.metric("⭐ Score", f"{score:.1%}")
                                with col2:
                                    st.metric("💰 Preço", f"R$ {rec.get('price', 0):,.0f}")
                                with col3:
                                    st.metric("⚡ RPM", f"{rec.get('rpm_capacity', 0):,}")
                                with col4:
                                    st.metric("📦 Tipo", rec.get('bearing_type', 'N/A'))
                                
                                st.divider()
                                
                                # Descrição
                                st.markdown("**📋 Descrição Técnica**")
                                st.caption(rec.get('technical_description', 'N/A'))
                                
                                # Info adicionais
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("📊 Carga", f"{rec.get('load_capacity', 0):,.0f} N")
                                with col2:
                                    st.metric("💵 Custo", f"R$ {rec.get('unit_cost', 0):,.2f}")
            
            except Exception as e:
                st.error(f"❌ Erro ao processar: {str(e)}")
                # LOGGING DE ERRO
                logger.error(f"❌ Erro ao gerar recomendações: {e}", exc_info=True)
                import traceback
                st.code(traceback.format_exc())

# ============================================================================
# HISTÓRICO RÁPIDO
# ============================================================================

if st.session_state.history:
    st.divider()
    
    with st.expander("📜 Histórico de Buscas Recentes"):
        for i, item in enumerate(reversed(st.session_state.history[-10:]), 1):
            timestamp = item.get('timestamp')
            
            if isinstance(timestamp, datetime):
                time_str = timestamp.strftime('%d/%m %H:%M')
            else:
                time_str = str(timestamp)
            
            query = item.get('query', 'N/A')[:60]
            st.caption(f"{i}. {query} • {item.get('count', 0)} resultados • {time_str}")

# ============================================================================
# SEÇÃO DE EXEMPLOS POR INDÚSTRIA
# ============================================================================

st.divider()

with st.expander("💡 Exemplos por Indústria", expanded=False):
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <p style="color: #94A3B8; font-size: 14px;">
            Explore exemplos práticos de como descrever problemas técnicos para cada setor industrial. 
            Clique em "Usar este exemplo" para inserir no campo de busca.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Iterar sobre cada indústria
    for industry, info in EXAMPLES_BY_INDUSTRY.items():
        st.markdown(f"### {industry}")
        st.caption(f"**Principal problema:** {info['principal_problema']}")
        
        # Exibir cada exemplo da indústria
        for idx, exemplo in enumerate(info['exemplos'], 1):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**Exemplo {idx}: {exemplo['titulo']}**")
                    st.code(exemplo['descricao'], language="text")
                
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento
                    # Criar key única baseada em hash para evitar conflitos
                    button_key = f"use_example_{hash(industry)}_{hash(exemplo['titulo'])}"
                    if st.button("📋 Usar", key=button_key, use_container_width=True):
                        st.session_state.user_query_value = exemplo['descricao']
                        st.rerun()

                        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Mensagem final
    st.info("💡 **Dica:** Adapte os exemplos conforme sua necessidade específica. Quanto mais detalhes você incluir, melhores serão os resultados!")

# ============================================================================
# FOOTER
# ============================================================================

render_footer()
        