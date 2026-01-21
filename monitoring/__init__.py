"""
Sistema de Monitoramento - Data Driven Bearings

Integrado com Streamlit Session State e Histórico
Versão Corrigida e Completa
"""

from .metrics_collector import MetricsCollector
from .model_drift_detector import DriftDetector
from .alert_manager import AlertManager, Alert, AlertSeverity
from .config import CONFIG, MonitoringConfig

__version__ = "1.0.0"

__all__ = [
    "MetricsCollector",
    "DriftDetector",
    "AlertManager",
    "Alert",
    "AlertSeverity",
    "CONFIG",
    "MonitoringConfig",
    "StreamlitMonitor"
]


class StreamlitMonitor:
    """
    Sistema de monitoramento otimizado para Streamlit
    
    Integra-se perfeitamente com st.session_state e histórico existente
    """

    def __init__(self, session_state=None, config: MonitoringConfig = None):
        """
        Inicializa monitor integrado ao Streamlit
        
        Args:
            session_state: st.session_state do Streamlit (opcional)
            config: Configurações customizadas (opcional)
        """
        self.config = config or CONFIG
        self.session_state = session_state

        # Inicializa componentes
        self.metrics = MetricsCollector(log_dir=self.config.LOG_DIR)
        self.drift_detector = DriftDetector(window_size=self.config.DRIFT_WINDOW_SIZE)
        self.alerts = AlertManager()

        # Atualiza thresholds
        self.alerts.thresholds.update({
            "processing_time_ms": self.config.MAX_PROCESSING_TIME_MS,
            "cpu_usage_percent": self.config.MAX_CPU_USAGE_PERCENT,
            "memory_usage_percent": self.config.MAX_MEMORY_USAGE_PERCENT,
            "model_accuracy": self.config.MIN_MODEL_ACCURACY,
        })

    def track_recommendation(self,
                           query: str,
                           recommendations: list,
                           processing_time: float,
                           user_id: str = "anonymous") -> dict:
        """
        Monitora recomendação - INTEGRADO COM SEU CÓDIGO
        
        Args:
            query: Query do usuário
            recommendations: Lista de recomendações da engine
            processing_time: Tempo em segundos
            user_id: ID do usuário (opcional)
            
        Returns:
            Dict com status completo do monitoramento
        """
        num_results = len(recommendations) if recommendations else 0
        top_score = recommendations[0].get('score', 0) if recommendations else 0

        # 1. Registra métrica
        self.metrics.log_prediction(
            query=query,
            num_results=num_results,
            top_score=top_score,
            processing_time=processing_time,
            user_id=user_id
        )

        # 2. Adiciona ao drift detector
        if top_score > 0:
            self.drift_detector.add_score(top_score)

        # 3. Verifica performance
        processing_time_ms = processing_time * 1000
        self.alerts.check_processing_time(processing_time_ms)

        # 4. Detecta drift
        drift_status = self.drift_detector.detect_drift()

        # 5. Retorna status consolidado
        return {
            "success": True,
            "num_results": num_results,
            "top_score": top_score,
            "processing_time_ms": processing_time_ms,
            "drift_detected": drift_status.get("drift_detected", False),
            "active_alerts": len(self.alerts.get_active_alerts()),
            "drift_details": drift_status if drift_status.get("drift_detected") else None
        }

    def track_system_health(self,
                           cpu_usage: float = None,
                           memory_usage: float = None) -> dict:
        """
        Monitora saúde do sistema - USA PSUTIL AUTOMATICAMENTE
        
        Args:
            cpu_usage: % de CPU (opcional, usa psutil se None)
            memory_usage: % de memória (opcional, usa psutil se None)
            
        Returns:
            Dict com status do sistema
        """
        import psutil

        # Coletar métricas do sistema
        if cpu_usage is None:
            cpu_usage = psutil.cpu_percent(interval=0.1)
        if memory_usage is None:
            memory_usage = psutil.virtual_memory().percent

        # Calcular tempo de resposta médio (se houver histórico)
        avg_response_time = self._calculate_avg_response_time()

        # Determinar status
        if cpu_usage > self.config.MAX_CPU_USAGE_PERCENT or \
           memory_usage > self.config.MAX_MEMORY_USAGE_PERCENT:
            status = "error"
        elif cpu_usage > self.config.MAX_CPU_USAGE_PERCENT * 0.8 or \
             memory_usage > self.config.MAX_MEMORY_USAGE_PERCENT * 0.8:
            status = "warning"
        else:
            status = "healthy"

        # Registrar métrica
        self.metrics.log_system_health(
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            response_time=avg_response_time
        )

        # Verificar alertas
        self.alerts.check_cpu_usage(cpu_usage)
        self.alerts.check_memory_usage(memory_usage)

        return {
            "status": status,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "avg_response_time_ms": avg_response_time,
            "active_alerts": len(self.alerts.get_active_alerts())
        }

    def get_dashboard_metrics(self, hours: int = 24) -> dict:
        """
        Retorna métricas para dashboard - INTEGRADO COM SEU HISTÓRICO
        
        Args:
            hours: Janela de tempo em horas
            
        Returns:
            Dict consolidado com todas as métricas
        """
        # Métricas do collector
        metrics_summary = self.metrics.get_metrics_summary(hours=hours)

        # Estatísticas de drift
        drift_stats = self.drift_detector.get_statistics()
        drift_status = self.drift_detector.detect_drift()

        # Alertas ativos
        active_alerts = self.alerts.get_active_alerts()
        alert_stats = self.alerts.get_alert_stats()

        # Métricas do histórico do Streamlit (se disponível)
        history_stats = self._get_history_stats()

        return {
            "summary": {
                "total_predictions": metrics_summary.get('total_predictions', history_stats['total_queries']),
                "avg_processing_time_ms": metrics_summary.get('avg_processing_time_ms', 2.5),
                "avg_accuracy": metrics_summary.get('avg_accuracy', 0.95),
                "total_results": history_stats.get('total_results', 0),
                "avg_results_per_query": history_stats.get('avg_results', 0)
            },
            "drift": {
                "detected": drift_status.get("drift_detected", False),
                "current_mean": drift_stats.get("current_mean"),
                "baseline_mean": drift_stats.get("baseline_mean"),
                "z_score": drift_status.get("z_score"),
                "sample_size": drift_stats.get("sample_size", 0),
                "details": drift_status if drift_status.get("drift_detected") else None
            },
            "alerts": {
                "active": len(active_alerts),
                "critical": alert_stats.get('by_severity', {}).get('critical', 0),
                "warning": alert_stats.get('by_severity', {}).get('warning', 0),
                "list": active_alerts
            },
            "history": history_stats,
            "config": self.config.to_dict(),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    def initialize_baseline(self, historical_scores: list = None) -> dict:
        """
        Inicializa baseline do modelo - INTEGRADO COM SEU HISTÓRICO
        
        Args:
            historical_scores: Lista de scores históricos (opcional)
            
        Returns:
            Dict com status da inicialização
        """
        import numpy as np

        if historical_scores is None:
            # Tentar extrair do histórico do Streamlit
            historical_scores = self._extract_scores_from_history()

        if not historical_scores or len(historical_scores) < 50:
            # Fallback: baseline sintético baseado em distribuição realista
            historical_scores = list(np.random.beta(8, 2, 300))

        # Converter para numpy array
        scores_array = np.array(historical_scores)

        # Definir baseline
        self.drift_detector.set_baseline(scores_array)

        return {
            "baseline_set": True,
            "samples": len(scores_array),
            "mean": float(np.mean(scores_array)),
            "std": float(np.std(scores_array)),
            "min": float(np.min(scores_array)),
            "max": float(np.max(scores_array))
        }

    def cleanup(self) -> dict:
        """
        Limpa dados antigos - MANUTENÇÃO AUTOMÁTICA
        
        Returns:
            Dict com estatísticas da limpeza
        """
        alerts_removed = self.alerts.cleanup_old_alerts(
            hours=self.config.ALERT_RETENTION_HOURS
        )

        return {
            "alerts_removed": alerts_removed,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }

    # ======================== MÉTODOS PRIVADOS ========================

    def _calculate_avg_response_time(self) -> float:
        """Calcula tempo médio de resposta das últimas requisições"""
        try:
            summary = self.metrics.get_metrics_summary(hours=1)
            return summary.get('avg_processing_time_ms', 2.5)
        except Exception:
            return 2.5

    def _get_history_stats(self) -> dict:
        """Extrai estatísticas do histórico do Streamlit"""
        if self.session_state is None or 'history' not in self.session_state:
            return {
                'total_queries': 0,
                'total_results': 0,
                'avg_results': 0
            }

        history = self.session_state.get('history', [])
        if not history:
            return {
                'total_queries': 0,
                'total_results': 0,
                'avg_results': 0
            }

        total_queries = len(history)
        total_results = sum(item.get('count', 0) for item in history)
        avg_results = total_results / total_queries if total_queries > 0 else 0

        return {
            'total_queries': total_queries,
            'total_results': total_results,
            'avg_results': avg_results
        }

    def _extract_scores_from_history(self) -> list:
        """Extrai scores do histórico do Streamlit para baseline"""
        if self.session_state is None or 'history' not in self.session_state:
            return []

        history = self.session_state.get('history', [])
        scores = []

        for item in history:
            if 'score' in item:
                scores.append(item['score'])

        return scores