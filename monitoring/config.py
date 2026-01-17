"""
Configurações de Monitoramento - DDF Tech 2025
Centraliza thresholds e configurações
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class MonitoringConfig:
    """Configurações centralizadas de monitoramento"""
    
    # Thresholds de Performance
    MAX_PROCESSING_TIME_MS: float = 5000  # 5 segundos
    MAX_CPU_USAGE_PERCENT: float = 80
    MAX_MEMORY_USAGE_PERCENT: float = 85
    MIN_MODEL_ACCURACY: float = 0.85
    MIN_PREDICTIONS_PER_HOUR: int = 10
    
    # Thresholds de Drift
    DRIFT_Z_SCORE_THRESHOLD: float = 2.0
    DRIFT_VARIANCE_RATIO_THRESHOLD: float = 2.0
    DRIFT_WINDOW_SIZE: int = 100
    
    # Configurações de Logs
    LOG_DIR: str = "logs"
    METRICS_FILE: str = "metrics.jsonl"
    LOG_LEVEL: str = "INFO"
    
    # Configurações de Alertas
    ALERT_RETENTION_HOURS: int = 48
    ENABLE_EMAIL_ALERTS: bool = False
    ALERT_EMAIL: str = "cryslaynecinara0231@gmail.com"
    
    def to_dict(self) -> Dict:
        """Converte config para dicionário"""
        return {
            "performance": {
                "max_processing_time_ms": self.MAX_PROCESSING_TIME_MS,
                "max_cpu_percent": self.MAX_CPU_USAGE_PERCENT,
                "max_memory_percent": self.MAX_MEMORY_USAGE_PERCENT,
                "min_accuracy": self.MIN_MODEL_ACCURACY
            },
            "drift": {
                "z_score_threshold": self.DRIFT_Z_SCORE_THRESHOLD,
                "variance_ratio_threshold": self.DRIFT_VARIANCE_RATIO_THRESHOLD,
                "window_size": self.DRIFT_WINDOW_SIZE
            },
            "alerts": {
                "retention_hours": self.ALERT_RETENTION_HOURS,
                "email_enabled": self.ENABLE_EMAIL_ALERTS
            }
        }

# Instância global
CONFIG = MonitoringConfig()