"""
Sistema de Coleta de Métricas - Data Driven Bearings
Monitora performance do modelo e saúde do sistema
"""
import json
from datetime import datetime
from typing import Dict, Any
import os
import pandas as pd

from utils.logger import setup_logger

logger = setup_logger("metrics_collector", log_file="logs/metrics_collector.log")

class MetricsCollector:
    """Coleta e armazena métricas de performance"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.metrics_file = os.path.join(log_dir, "metrics.jsonl")
        os.makedirs(log_dir, exist_ok=True)
        
    def log_prediction(self, 
                      query: str, 
                      num_results: int, 
                      top_score: float,
                      processing_time: float,
                      user_id: str = "anonymous") -> None:
        """Registra uma predição"""
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "prediction",
            "user_id": user_id,
            "query_length": len(query),
            "num_results": num_results,
            "top_score": float(top_score),
            "processing_time_ms": float(processing_time * 1000),
            "query_preview": query[:100]  # Apenas preview para privacidade
        }
        
        self._save_metric(metric)
        logger.info(f"Prediction logged: {num_results} results in {processing_time*1000:.2f}ms")
    
    def log_user_feedback(self, 
                         prediction_id: str, 
                         feedback: str,  # "positive", "negative", "neutral"
                         rating: int) -> None:  # 1-5
        """Registra feedback do usuário"""
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "user_feedback",
            "prediction_id": prediction_id,
            "feedback": feedback,
            "rating": int(rating)
        }
        
        self._save_metric(metric)
        logger.info(f"User feedback: {feedback} with rating {rating}")
    
    def log_system_health(self,
                         status: str,  # "healthy", "warning", "error"
                         cpu_usage: float,
                         memory_usage: float,
                         response_time: float) -> None:
        """Registra saúde do sistema"""
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "system_health",
            "status": status,
            "cpu_usage_percent": float(cpu_usage),
            "memory_usage_percent": float(memory_usage),
            "response_time_ms": float(response_time)
        }
        
        self._save_metric(metric)
        logger.info(f"System health: {status} - CPU: {cpu_usage:.1f}% - Memory: {memory_usage:.1f}%")
    
    def log_model_performance(self,
                             accuracy: float,
                             precision: float,
                             recall: float,
                             f1_score: float) -> None:
        """Registra performance do modelo"""
        
        metric = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "model_performance",
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1_score)
        }
        
        self._save_metric(metric)
        logger.info(f"Model performance - Accuracy: {accuracy:.1%} | F1: {f1_score:.1%}")
    
    def _save_metric(self, metric: Dict[str, Any]) -> None:
        """Salva métrica em arquivo JSONL"""
        try:
            with open(self.metrics_file, 'a') as f:
                f.write(json.dumps(metric) + '\n')
        except Exception as e:
            logger.error(f"Erro ao salvar métrica: {e}")
    
    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Retorna resumo de métricas das últimas N horas"""
        
        try:
            metrics = []
            cutoff_time = pd.Timestamp.now() - pd.Timedelta(hours=hours)
            
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            m = json.loads(line)
                            if pd.Timestamp(m['timestamp']) > cutoff_time:
                                metrics.append(m)
            
            if not metrics:
                return {"status": "no_data"}
            
            df = pd.DataFrame(metrics)
            
            return {
                "total_predictions": len(df[df['event_type'] == 'prediction']),
                "avg_processing_time_ms": df[df['event_type'] == 'prediction']['processing_time_ms'].mean(),
                "total_feedback": len(df[df['event_type'] == 'user_feedback']),
                "avg_user_rating": df[df['event_type'] == 'user_feedback']['rating'].mean(),
                "system_health_status": df[df['event_type'] == 'system_health']['status'].value_counts().to_dict(),
                "avg_accuracy": df[df['event_type'] == 'model_performance']['accuracy'].mean(),
            }
        
        except Exception as e:
            logger.error(f"Erro ao gerar resumo: {e}")
            return {"status": "error", "error": str(e)}
