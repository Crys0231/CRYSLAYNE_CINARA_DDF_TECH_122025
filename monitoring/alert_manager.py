"""
Sistema de Alertas - DDF Tech 2025
Notifica sobre problemas de performance
"""
import logging
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class Alert:
    def __init__(self, 
                 title: str,
                 message: str,
                 severity: AlertSeverity,
                 metric_name: str,
                 current_value: float,
                 threshold: float):
        self.id = datetime.now().isoformat()
        self.title = title
        self.message = message
        self.severity = severity
        self.metric_name = metric_name
        self.current_value = current_value
        self.threshold = threshold
        self.timestamp = datetime.now()
        self.resolved = False
    
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
            "resolved": self.resolved
        }

class AlertManager:
    """Gerencia alertas do sistema"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
        self.thresholds = {
            "processing_time_ms": 5000,        # > 5s é problema
            "cpu_usage_percent": 80,           # > 80% é problema
            "memory_usage_percent": 85,        # > 85% é problema
            "model_accuracy": 0.85,            # < 85% é problema
            "predictions_per_hour": 10,        # < 10/hora é baixo
        }
    
    def check_processing_time(self, processing_time_ms: float) -> None:
        """Verifica se tempo de processamento está alto"""
        
        if processing_time_ms > self.thresholds["processing_time_ms"]:
            alert = Alert(
                title="⚠️ Tempo de Processamento Alto",
                message=f"Predição levou {processing_time_ms:.0f}ms (limite: {self.thresholds['processing_time_ms']}ms)",
                severity=AlertSeverity.WARNING,
                metric_name="processing_time_ms",
                current_value=processing_time_ms,
                threshold=self.thresholds["processing_time_ms"]
            )
            self.alerts.append(alert)
            logger.warning(f"ALERTA: {alert.message}")
    
    def check_cpu_usage(self, cpu_usage: float) -> None:
        """Verifica uso de CPU"""
        
        if cpu_usage > self.thresholds["cpu_usage_percent"]:
            alert = Alert(
                title="🔴 CPU Elevada",
                message=f"CPU em {cpu_usage:.1f}% (limite: {self.thresholds['cpu_usage_percent']}%)",
                severity=AlertSeverity.CRITICAL,
                metric_name="cpu_usage_percent",
                current_value=cpu_usage,
                threshold=self.thresholds["cpu_usage_percent"]
            )
            self.alerts.append(alert)
            logger.critical(f"ALERTA CRÍTICO: {alert.message}")
    
    def check_memory_usage(self, memory_usage: float) -> None:
        """Verifica uso de memória"""
        
        if memory_usage > self.thresholds["memory_usage_percent"]:
            alert = Alert(
                title="🔴 Memória Elevada",
                message=f"Memória em {memory_usage:.1f}% (limite: {self.thresholds['memory_usage_percent']}%)",
                severity=AlertSeverity.CRITICAL,
                metric_name="memory_usage_percent",
                current_value=memory_usage,
                threshold=self.thresholds["memory_usage_percent"]
            )
            self.alerts.append(alert)
            logger.critical(f"ALERTA CRÍTICO: {alert.message}")
    
    def check_model_accuracy(self, accuracy: float) -> None:
        """Verifica se modelo degradou"""
        
        if accuracy < self.thresholds["model_accuracy"]:
            alert = Alert(
                title="📉 Degradação do Modelo",
                message=f"Acurácia caiu para {accuracy:.1%} (baseline: {self.thresholds['model_accuracy']:.0%})",
                severity=AlertSeverity.CRITICAL,
                metric_name="model_accuracy",
                current_value=accuracy,
                threshold=self.thresholds["model_accuracy"]
            )
            self.alerts.append(alert)
            logger.critical(f"ALERTA CRÍTICO: {alert.message}")
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Retorna alertas não resolvidos"""
        return [a.to_dict() for a in self.alerts if not a.resolved]
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Marca alerta como resolvido"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                return True
        return False
