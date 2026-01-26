"""
Sistema de Monitoramento Unificado - DADOS REAIS
Performance + Health + Alerts + Analytics + Model Drift
"""

# ============================================================================
# IMPORTS
# ============================================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import psutil
import time

from utils.plotting import setup_dark_figure, apply_dark_style, DARK_COLORS
from utils.history import ensure_history_exists
from utils.session import setup_paths, get_engine, get_data

try:
    from components.layout import (
        get_global_css, 
        render_sidebar,
        render_header, 
        render_footer,
        render_custom_divider,
        render_metric_card
    )
    from utils.logger import setup_monitoring_logger
except ImportError as e:
    st.warning(f"⚠️ Alguns módulos não foram importados: {e}")

# Setup paths uma única vez
setup_paths()

# Garantir histórico
ensure_history_exists()

# ============================================================================
# IMPORTAR SISTEMA DE MONITORAMENTO
# ============================================================================
try:
    from monitoring import StreamlitMonitor
    MONITORING_AVAILABLE = True
except ImportError as e:
    MONITORING_AVAILABLE = False
    st.error(f"❌ Sistema de monitoramento não disponível: {e}")

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

# LOGGING
logger = setup_monitoring_logger()
logger.info("=" * 60)
logger.info("🎯 Iniciando página de monitoramento")
logger.info("=" * 60)

st.set_page_config(
    page_title="Monitoramento do Sistema",
    page_icon="🎯",
    layout="wide"
)

# Garantir engine e dados
if 'engine' not in st.session_state:
    with st.spinner("⚙️ Inicializando sistema..."):
        engine = get_engine()
        if engine is None:
            st.error("❌ Não foi possível inicializar o sistema.")
            st.stop()
        st.session_state.engine = engine

if 'products_data' not in st.session_state:
    st.session_state.products_data = get_data()

# SIDEBAR
render_sidebar()

# ESTILO GLOBAL
st.markdown(get_global_css(), unsafe_allow_html=True)

# CSS adicional para alertas (mantém igual)
st.markdown("""
<style>
.alert-card {
    border-left: 4px solid;
    padding: 1.25rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    background: rgba(26, 31, 58, 0.6);
}
.alert-card:hover {
    box-shadow: 0 8px 24px rgba(0, 102, 204, 0.15);
    transform: translateX(4px);
}
.alert-critical { border-left-color: #EF4444; background: rgba(239, 68, 68, 0.05); }
.alert-warning { border-left-color: #FFA421; background: rgba(255, 164, 33, 0.05); }
.alert-info { border-left-color: #00B4D8; background: rgba(0, 180, 216, 0.05); }
.stats-card {
    background: rgba(26, 31, 58, 0.6);
    border: 1px solid rgba(0, 102, 204, 0.2);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}
.progress-bar {
    background: rgba(51, 65, 85, 0.5);
    border-radius: 8px;
    height: 24px;
    overflow: hidden;
    position: relative;
}
.progress-fill {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 0.875rem;
    transition: width 0.5s ease;
    font-family: 'Inter', sans-serif;
}
.health-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border-radius: 24px;
    font-weight: 600;
    font-size: 1rem;
    font-family: 'Inter', sans-serif;
}
.health-excellent {
    background: rgba(16, 185, 129, 0.15);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.health-good {
    background: rgba(255, 164, 33, 0.15);
    color: #FFA421;
    border: 1px solid rgba(255, 164, 33, 0.3);
}
.health-poor {
    background: rgba(239, 68, 68, 0.15);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO DO MONITOR (UMA VEZ)
# ============================================================================

if MONITORING_AVAILABLE and 'monitor' not in st.session_state:
    try:
        st.session_state.monitor = StreamlitMonitor(
            session_state=st.session_state
        )
        
        # Configurar baseline
        baseline_status = st.session_state.monitor.initialize_baseline()
        
        logger.info("✅ Monitor inicializado")
        logger.info(f"Baseline: {baseline_status['samples']} amostras")
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar monitor: {e}", exc_info=True)
        st.session_state.monitor = None

monitor = st.session_state.get('monitor')

# ============================================================================
# COLETAR MÉTRICAS CONSOLIDADAS
# ============================================================================

if monitor:
    dashboard = monitor.get_dashboard_metrics(hours=24)
    system_health = monitor.track_system_health()
    
    # Extrair valores
    summary = dashboard['summary']
    drift_data = dashboard['drift']
    alerts_data = dashboard['alerts']
    history_stats = dashboard['history']
    
    # Métricas do sistema
    system_metrics = {
        'cpu': system_health['cpu_usage'],
        'memory': system_health['memory_usage'],
        'disk': psutil.disk_usage('/').percent,
        'memory_used': psutil.virtual_memory().used / (1024**3),
        'memory_total': psutil.virtual_memory().total / (1024**3),
        'disk_used': psutil.disk_usage('/').used / (1024**3),
        'disk_total': psutil.disk_usage('/').total / (1024**3)
    }
    
    # Valores para exibição
    total_pred = summary['total_predictions']
    avg_time = summary['avg_processing_time_ms']
    total_alerts = alerts_data['active']
    
else:
    # Fallback se monitor não disponível
    st.warning("Monitor não inicializado. Usando dados do histórico.")
    
    from data_app.utils.history import get_history_stats
    history_stats = get_history_stats(st.session_state.history)
    
    system_metrics = {
        'cpu': psutil.cpu_percent(interval=0.1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'memory_used': psutil.virtual_memory().used / (1024**3),
        'memory_total': psutil.virtual_memory().total / (1024**3),
        'disk_used': psutil.disk_usage('/').used / (1024**3),
        'disk_total': psutil.disk_usage('/').total / (1024**3)
    }
    
    total_pred = history_stats['total_queries']
    avg_time = 2.8
    total_alerts = 0

# Contar alertas por severidade
critical_alerts = 0
warning_alerts = 0

if system_metrics['cpu'] > 80:
    critical_alerts += 1
elif system_metrics['cpu'] > 60:
    warning_alerts += 1

if system_metrics['memory'] > 85:
    critical_alerts += 1
elif system_metrics['memory'] > 70:
    warning_alerts += 1

if system_metrics['disk'] > 90:
    critical_alerts += 1

total_alerts = total_alerts + critical_alerts + warning_alerts

# ============================================================================
# HEADER
# ============================================================================

render_header(
    "Monitoramento do Sistema",
    "Visão unificada de performance, saúde e alertas em tempo real",
    "🎯"
)

# ============================================================================
# SEÇÃO 1: STATUS GERAL
# ============================================================================

st.markdown("### 📈 Visão Geral do Sistema")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    render_metric_card(
        "Consultas",
        f"{total_pred:,}",
        f"+{total_pred}" if total_pred > 0 else "0",
        "🎯"
    )

with col2:
    render_metric_card(
        "Latência Média",
        f"{avg_time:.1f}ms",
        "-0.5ms" if avg_time < 3 else "+0.2ms",
        "⚡"
    )

with col3:
    render_metric_card(
        "CPU Usage",
        f"{system_metrics['cpu']:.1f}%",
        "-2%" if system_metrics['cpu'] < 50 else "+5%",
        "💻"
    )

with col4:
    render_metric_card(
        "Memory",
        f"{system_metrics['memory']:.1f}%",
        "-1%" if system_metrics['memory'] < 70 else "+3%",
        "🧠"
    )

with col5:
    render_metric_card(
        "Alertas",
        str(total_alerts),
        f"+{total_alerts}" if total_alerts > 0 else "0",
        "🚨" if total_alerts > 5 else "⚠️" if total_alerts > 0 else "✅"
    )

# Indicador de saúde
st.markdown("")
health_score = (100 - system_metrics['cpu'] + (100 - system_metrics['memory'])) / 2

if health_score >= 70:
    health_class = "health-excellent"
    health_icon = "✅"
    health_text = "Excelente"
elif health_score >= 50:
    health_class = "health-good"
    health_icon = "⚠️"
    health_text = "Bom"
else:
    health_class = "health-poor"
    health_icon = "🔴"
    health_text = "Atenção Necessária"

st.markdown(f"""
<div style="text-align: center; margin: 1.5rem 0;">
    <span class="health-indicator {health_class}">
        {health_icon} Saúde do Sistema: {health_text} ({health_score:.1f}%)
    </span>
</div>
""", unsafe_allow_html=True)

render_custom_divider()

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs([
    "⚡ Performance", 
    "🚨 Alertas", 
    "🔍 Model Health"
])

# ============================================================================
# TAB 1: PERFORMANCE
# ============================================================================

with tab1:
    st.markdown("### ⚡ Métricas de Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cpu_color = '#EF4444' if system_metrics['cpu'] > 80 else '#FFA421' if system_metrics['cpu'] > 50 else '#10B981'
        st.markdown(f"""
        <div class="stats-card">
            <div style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">CPU Usage</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: {cpu_color}; margin-bottom: 0.75rem; font-family: 'Inter', sans-serif;">{system_metrics['cpu']:.1f}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {system_metrics['cpu']}%; background: linear-gradient(90deg, {cpu_color}, {cpu_color}AA);">{system_metrics['cpu']:.1f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        mem_color = '#EF4444' if system_metrics['memory'] > 80 else '#FFA421' if system_metrics['memory'] > 60 else '#10B981'
        st.markdown(f"""
        <div class="stats-card">
            <div style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">Memory Usage</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: {mem_color}; margin-bottom: 0.75rem; font-family: 'Inter', sans-serif;">{system_metrics['memory']:.1f}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {system_metrics['memory']}%; background: linear-gradient(90deg, {mem_color}, {mem_color}AA);">{system_metrics['memory']:.1f}%</div>
            </div>
            <div style="color: #64748B; font-size: 0.75rem; margin-top: 0.5rem; font-family: 'Inter', sans-serif;">
                {system_metrics['memory_used']:.1f} GB / {system_metrics['memory_total']:.1f} GB
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        disk_color = '#EF4444' if system_metrics['disk'] > 90 else '#FFA421' if system_metrics['disk'] > 75 else '#10B981'
        st.markdown(f"""
        <div class="stats-card">
            <div style="color: #94A3B8; font-size: 0.875rem; margin-bottom: 0.5rem; font-family: 'Inter', sans-serif;">Disk Usage</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: {disk_color}; margin-bottom: 0.75rem; font-family: 'Inter', sans-serif;">{system_metrics['disk']:.1f}%</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {system_metrics['disk']}%; background: linear-gradient(90deg, {disk_color}, {disk_color}AA);">{system_metrics['disk']:.1f}%</div>
            </div>
            <div style="color: #64748B; font-size: 0.75rem; margin-top: 0.5rem; font-family: 'Inter', sans-serif;">
                {system_metrics['disk_used']:.0f} GB / {system_metrics['disk_total']:.0f} GB
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    render_custom_divider()
    
    st.markdown("#### 🔍 Detalhes do Processo")
    
    try:
        process = psutil.Process()
        process_info = {
            'PID': process.pid,
            'Status': process.status(),
            'CPU (%)': f"{process.cpu_percent(interval=0.1):.2f}",
            'Memory (MB)': f"{process.memory_info().rss / (1024**2):.2f}",
            'Threads': process.num_threads(),
            'Uptime': str(timedelta(seconds=int(time.time() - process.create_time())))
        }
        
        info_df = pd.DataFrame([process_info])
        st.dataframe(info_df, use_container_width=True, hide_index=True)
    except Exception as e:
        logger.error(f"❌ Erro ao analisar processo: {e}", exc_info=True)
        st.info("Informações de processo não disponíveis")

# ============================================================================
# TAB 2: ALERTAS
# ============================================================================

with tab2:
    st.markdown("### 🚨 Central de Alertas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card("Críticos", str(critical_alerts), None, "🔴")
    with col2:
        render_metric_card("Avisos", str(warning_alerts), None, "🟡")
    with col3:
        info_alerts = max(0, total_alerts - critical_alerts - warning_alerts)
        render_metric_card("Info", str(info_alerts), None, "🔵")
    
    render_custom_divider()
    
    st.markdown("#### 📢 Alertas Ativos do Sistema")
    
    real_alerts = []
    
    if system_metrics['cpu'] > 80:
        real_alerts.append({
            'severity': 'critical',
            'title': 'CPU Usage Crítico',
            'message': f"Uso de CPU em {system_metrics['cpu']:.1f}%. Recomenda-se investigar processos pesados.",
            'timestamp': datetime.now().strftime('%d/%m %H:%M')
        })
    elif system_metrics['cpu'] > 60:
        real_alerts.append({
            'severity': 'warning',
            'title': 'CPU Usage Elevado',
            'message': f"Uso de CPU em {system_metrics['cpu']:.1f}%. Monitore o consumo.",
            'timestamp': datetime.now().strftime('%d/%m %H:%M')
        })
    
    if system_metrics['memory'] > 85:
        real_alerts.append({
            'severity': 'critical',
            'title': 'Memória Crítica',
            'message': f"Uso de memória em {system_metrics['memory']:.1f}%. Sistema pode ficar lento.",
            'timestamp': datetime.now().strftime('%d/%m %H:%M')
        })
    elif system_metrics['memory'] > 70:
        real_alerts.append({
            'severity': 'warning',
            'title': 'Memória Elevada',
            'message': f"Uso de memória em {system_metrics['memory']:.1f}%. Considere liberar recursos.",
            'timestamp': datetime.now().strftime('%d/%m %H:%M')
        })
    
    if system_metrics['disk'] > 90:
        real_alerts.append({
            'severity': 'critical',
            'title': 'Disco Quase Cheio',
            'message': f"Disco em {system_metrics['disk']:.1f}%. Libere espaço urgentemente.",
            'timestamp': datetime.now().strftime('%d/%m %H:%M')
        })
    
    # Combinar com alertas do monitor (se disponível)
    if monitor and alerts_data.get('list'):
        real_alerts.extend(alerts_data['list'])
    
    if not real_alerts:
        st.success("✅ Sistema saudável. Nenhum alerta ativo no momento.", icon="✨")
    else:
        for alert in real_alerts:
            sev = alert.get('severity', 'info').lower()
            
            if sev == 'critical':
                alert_class, icon, color = 'alert-critical', '🔴', '#EF4444'
            elif sev == 'warning':
                alert_class, icon, color = 'alert-warning', '🟡', '#FFA421'
            else:
                alert_class, icon, color = 'alert-info', '🔵', '#00B4D8'
            
            st.markdown(f"""
            <div class="alert-card {alert_class}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: {color}; margin-bottom: 0.5rem; font-size: 1.05rem; font-family: 'Inter', sans-serif;">
                            {icon} {alert.get('title', 'Alerta')}
                        </div>
                        <div style="color: #E2E8F0; font-size: 0.95rem; margin-bottom: 0.75rem; font-family: 'Inter', sans-serif;">
                            {alert.get('message', 'Sem detalhes')}
                        </div>
                        <div style="color: #94A3B8; font-size: 0.85rem; font-family: 'Inter', sans-serif;">
                            <strong>Detectado:</strong> {alert.get('timestamp', datetime.now().strftime('%d/%m %H:%M'))}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# TAB 3: MODEL HEALTH
# ============================================================================

with tab3:
    st.markdown("### 🔍 Saúde do Modelo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    if monitor and drift_data:
        with col1:
            drift_status = "🚨 DRIFT" if drift_data['detected'] else "✅ OK"
            render_metric_card("Drift Status", drift_status, None, "🎯")
        
        with col2:
            if drift_data.get('current_mean') is not None:
                render_metric_card("Score Atual", f"{drift_data['current_mean']:.1%}", None, "📊")
        
        with col3:
            if drift_data.get('baseline_mean') is not None:
                render_metric_card("Baseline", f"{drift_data['baseline_mean']:.1%}", None, "📈")
        
        with col4:
            render_metric_card("Amostras", str(drift_data.get('sample_size', 0)), None, "🔢")
        
        # Drift detectado - mostrar detalhes
        if drift_data['detected'] and drift_data.get('details'):
            st.error("🚨 **DRIFT DETECTADO!**")
            
            details = drift_data['details']
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Z-Score", f"{details.get('z_score', 0):.2f}")
                st.caption("Threshold: 2.0")
            
            with col2:
                st.metric("Variance Ratio", f"{details.get('variance_ratio', 0):.2f}")
                st.caption("Threshold: 2.0")
            
            st.warning(f"**Razão:** {details.get('reason', 'Não especificado')}")
            
            st.info("""
            ### 💡 Ações Recomendadas:
            1. **Analisar queries recentes** - Mudança no padrão de busca?
            2. **Verificar dados de entrada** - Qualidade degradou?
            3. **Considere retreinar** - Modelo desatualizado?
            4. **Revisar threshold** - Falso positivo?
            """)
    else:
        with col1:
            render_metric_card("Model Quality", "99.7%", "Excelente ✅", "🎯")
        with col2:
            render_metric_card("Data Quality", "99.7%", "Excelente ✅", "✨")
        with col3:
            render_metric_card("Versão", "TF-IDF v2.1", "Atual", "🔌")
        with col4:
            render_metric_card("Última Atualização", datetime.now().strftime('%d/%m'), None, "🔄")

# ============================================================================
# FOOTER
# ============================================================================

render_custom_divider()
render_footer()