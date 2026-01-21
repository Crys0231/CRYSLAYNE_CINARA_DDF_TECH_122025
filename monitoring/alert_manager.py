"""
Sistema de Alertas - Data Driven Bearings
VERSÃO CORRIGIDA - Previne alertas duplicados
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum
import json
import os

try:
    from utils.logger import setup_logger
    logger = setup_logger("alert_manager", log_file="logs/alerts.log")
except ImportError:
    import logging
    logger = logging.getLogger("alert_manager")
    logger.setLevel(logging.INFO)

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    
    def __lt__(self, other):
        severity_order = {"info": 0, "warning": 1, "critical": 2}
        return severity_order[self.value] < severity_order[other.value]

class Alert:
    def __init__(self, 
                 title: str,
                 message: str,
                 severity: AlertSeverity,
                 metric_name: str,
                 current_value: float,
                 threshold: float):
        self.id = f"{metric_name}_{severity.value}_{int(datetime.now().timestamp())}"
        self.title = title
        self.message = message
        self.severity = severity
        self.metric_name = metric_name
        self.current_value = current_value
        self.threshold = threshold
        self.timestamp = datetime.now()
        self.resolved = False
        self.resolved_at = None
        self.notes = ""
        self.cooldown_minutes = 5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "severity": self.severity.value,
            "metric": self.metric_name,
            "current_value": self.current_value,
            "threshold": self.threshold,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "notes": self.notes
        }
    
    def resolve(self, notes: str = "") -> None:
        """Marca alerta como resolvido"""
        self.resolved = True
        self.resolved_at = datetime.now()
        self.notes = notes

class AlertManager:
    """Gerencia alertas do sistema - VERSÃO CORRIGIDA"""
    
    def __init__(self, alerts_file: str = "logs/alerts.json"):
        self.alerts: List[Alert] = []
        self.alerts_file = alerts_file
        self.thresholds = {
            "processing_time_ms": 5000,
            "cpu_usage_percent": 80,
            "memory_usage_percent": 85,
            "model_accuracy": 0.85,
            "predictions_per_hour": 10,
        }
        
        # Cache de alertas recentes para evitar duplicatas
        self._recent_alerts_cache = {}
        self._cache_duration_minutes = 5
        
        self._load_alerts()
    
    def _is_duplicate_alert(self, metric_name: str, severity: AlertSeverity) -> bool:
        """
        Evita alertas duplicados durante o período de cooldown
        """
        cache_key = f"{metric_name}_{severity.value}"
        
        if cache_key in self._recent_alerts_cache:
            last_alert_time = self._recent_alerts_cache[cache_key]
            cooldown = timedelta(minutes=self._cache_duration_minutes)
            
            if datetime.now() - last_alert_time < cooldown:
                logger.debug(f"Alerta duplicado ignorado: {cache_key}")
                return True
        
        # Atualiza cache
        self._recent_alerts_cache[cache_key] = datetime.now()
        return False
    
    def _auto_resolve_old_alerts(self, metric_name: str) -> None:
        """
        Quando a métrica volta ao normal, resolve alertas anteriores
        """
        for alert in self.alerts:
            if alert.metric_name == metric_name and not alert.resolved:
                # Resolve se tiver mais de 10 minutos
                if datetime.now() - alert.timestamp > timedelta(minutes=10):
                    alert.resolve("Auto-resolvido: métrica normalizada")
                    logger.info(f"Alerta auto-resolvido: {alert.id}")
    
    def check_processing_time(self, processing_time_ms: float) -> Optional[Alert]:
        """Verifica se tempo de processamento está alto - CORRIGIDO"""
        
        # Resolve alertas antigos se tempo voltou ao normal
        if processing_time_ms <= self.thresholds["processing_time_ms"]:
            self._auto_resolve_old_alerts("processing_time_ms")
            return None
        
        # Evita duplicatas
        if self._is_duplicate_alert("processing_time_ms", AlertSeverity.WARNING):
            return None
        
        alert = Alert(
            title="⚠️ Tempo de Processamento Alto",
            message=f"Predição levou {processing_time_ms:.0f}ms (limite: {self.thresholds['processing_time_ms']}ms)",
            severity=AlertSeverity.WARNING,
            metric_name="processing_time_ms",
            current_value=processing_time_ms,
            threshold=self.thresholds["processing_time_ms"]
        )
        self.alerts.append(alert)
        self._save_alerts()
        logger.warning(f"ALERTA: {alert.message}")
        return alert
    
    def check_cpu_usage(self, cpu_usage: float) -> Optional[Alert]:
        """Verifica uso de CPU - CORRIGIDO"""
        
        # Resolve alertas antigos se CPU voltou ao normal
        if cpu_usage <= self.thresholds["cpu_usage_percent"]:
            self._auto_resolve_old_alerts("cpu_usage_percent")
            return None
        
        # Evita duplicatas
        if self._is_duplicate_alert("cpu_usage_percent", AlertSeverity.CRITICAL):
            return None
        
        alert = Alert(
            title="🔴 CPU Elevada",
            message=f"CPU em {cpu_usage:.1f}% (limite: {self.thresholds['cpu_usage_percent']}%)",
            severity=AlertSeverity.CRITICAL,
            metric_name="cpu_usage_percent",
            current_value=cpu_usage,
            threshold=self.thresholds["cpu_usage_percent"]
        )
        self.alerts.append(alert)
        self._save_alerts()
        logger.critical(f"ALERTA CRÍTICO: {alert.message}")
        return alert
    
    def check_memory_usage(self, memory_usage: float) -> Optional[Alert]:
        """Verifica uso de memória - CORRIGIDO"""
        
        # Resolve alertas antigos se memória voltou ao normal
        if memory_usage <= self.thresholds["memory_usage_percent"]:
            self._auto_resolve_old_alerts("memory_usage_percent")
            return None
        
        # Evita duplicatas
        if self._is_duplicate_alert("memory_usage_percent", AlertSeverity.CRITICAL):
            return None
        
        alert = Alert(
            title="🔴 Memória Elevada",
            message=f"Memória em {memory_usage:.1f}% (limite: {self.thresholds['memory_usage_percent']}%)",
            severity=AlertSeverity.CRITICAL,
            metric_name="memory_usage_percent",
            current_value=memory_usage,
            threshold=self.thresholds["memory_usage_percent"]
        )
        self.alerts.append(alert)
        self._save_alerts()
        logger.critical(f"ALERTA CRÍTICO: {alert.message}")
        return alert
    
    def check_model_accuracy(self, accuracy: float) -> Optional[Alert]:
        """Verifica se modelo degradou - CORRIGIDO"""
        
        # Resolve alertas antigos se acurácia voltou ao normal
        if accuracy >= self.thresholds["model_accuracy"]:
            self._auto_resolve_old_alerts("model_accuracy")
            return None
        
        # Evita duplicatas
        if self._is_duplicate_alert("model_accuracy", AlertSeverity.CRITICAL):
            return None
        
        alert = Alert(
            title="📉 Degradação do Modelo",
            message=f"Acurácia caiu para {accuracy:.1%} (baseline: {self.thresholds['model_accuracy']:.0%})",
            severity=AlertSeverity.CRITICAL,
            metric_name="model_accuracy",
            current_value=accuracy,
            threshold=self.thresholds["model_accuracy"]
        )
        self.alerts.append(alert)
        self._save_alerts()
        logger.critical(f"ALERTA CRÍTICO: {alert.message}")
        return alert
    
    def get_active_alerts(self, severity: Optional[AlertSeverity] = None) -> List[Dict[str, Any]]:
        """
        Retorna alertas não resolvidos - CORRIGIDO
        
        Args:
            severity: Filtrar por severidade (opcional)
        """
        # Limpa alertas antigos automaticamente
        self.cleanup_old_alerts(hours=24)
        
        alerts = [a for a in self.alerts if not a.resolved]
        
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        
        # Remove duplicatas baseado no metric_name
        seen = set()
        unique_alerts = []
        for alert in sorted(alerts, key=lambda x: x.timestamp, reverse=True):
            key = f"{alert.metric_name}_{alert.severity.value}"
            if key not in seen:
                seen.add(key)
                unique_alerts.append(alert)
        
        return [a.to_dict() for a in sorted(unique_alerts, key=lambda x: x.severity, reverse=True)]
    
    def get_alert_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de alertas - CORRIGIDO"""
        # Considera apenas alertas não resolvidos
        active_alerts = [a for a in self.alerts if not a.resolved]
        total = len(self.alerts)
        active = len(active_alerts)
        resolved = total - active
        
        by_severity = {}
        for severity in AlertSeverity:
            count = len([a for a in active_alerts if a.severity == severity])
            by_severity[severity.value] = count
        
        return {
            "total_alerts": total,
            "active_alerts": active,
            "resolved_alerts": resolved,
            "by_severity": by_severity
        }
    
    def resolve_alert(self, alert_id: str, notes: str = "") -> bool:
        """Marca alerta como resolvido"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolve(notes)
                self._save_alerts()
                logger.info(f"Alerta {alert_id} resolvido: {notes}")
                return True
        return False
    
    def cleanup_old_alerts(self, hours: int = 48) -> int:
        """Remove alertas antigos resolvidos - CORRIGIDO"""
        cutoff = datetime.now() - timedelta(hours=hours)
        initial_count = len(self.alerts)
        
        # Remove apenas alertas RESOLVIDOS antigos
        self.alerts = [
            a for a in self.alerts 
            if not a.resolved or (a.resolved_at and a.resolved_at > cutoff)
        ]
        
        removed = initial_count - len(self.alerts)
        if removed > 0:
            self._save_alerts()
            logger.info(f"Removidos {removed} alertas antigos")
        
        # Limpa cache de alertas expirados
        now = datetime.now()
        self._recent_alerts_cache = {
            k: v for k, v in self._recent_alerts_cache.items()
            if now - v < timedelta(minutes=self._cache_duration_minutes)
        }
        
        return removed
    
    def _save_alerts(self) -> None:
        """Salva alertas em arquivo"""
        try:
            os.makedirs(os.path.dirname(self.alerts_file), exist_ok=True)
            with open(self.alerts_file, 'w') as f:
                json.dump([a.to_dict() for a in self.alerts], f, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar alertas: {e}")
    
    def _load_alerts(self) -> None:
        """Carrega alertas do arquivo"""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Carregados {len(data)} alertas do histórico")
        except Exception as e:
            logger.error(f"Erro ao carregar alertas: {e}")