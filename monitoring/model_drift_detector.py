"""
Detector de Model Drift - DDF Tech 2025
Identifica quando modelo está degradando
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DriftDetector:
    """Detecta degradação de performance (Model Drift)"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.prediction_scores = []
        self.baseline_mean = None
        self.baseline_std = None
    
    def set_baseline(self, baseline_scores: np.ndarray) -> None:
        """Define baseline de scores históricos"""
        self.baseline_mean = np.mean(baseline_scores)
        self.baseline_std = np.std(baseline_scores)
        logger.info(f"Baseline estabelecido: mean={self.baseline_mean:.3f}, std={self.baseline_std:.3f}")
    
    def add_score(self, score: float) -> None:
        """Adiciona novo score à janela"""
        self.prediction_scores.append(score)
        if len(self.prediction_scores) > self.window_size:
            self.prediction_scores.pop(0)
    
    def detect_drift(self) -> Dict[str, Any]:
        """Detecta se há drift estatístico"""
        
        if len(self.prediction_scores) < 10 or self.baseline_mean is None:
            return {"drift_detected": False, "reason": "Dados insuficientes"}
        
        current_scores = np.array(self.prediction_scores)
        current_mean = np.mean(current_scores)
        current_std = np.std(current_scores)
        
        # Teste de mudança na média (Z-score)
        z_score = abs(current_mean - self.baseline_mean) / (self.baseline_std + 1e-6)
        
        # Teste de mudança na variância
        variance_ratio = current_std / (self.baseline_std + 1e-6)
        
        drift_detected = z_score > 2.0 or variance_ratio > 2.0
        
        result = {
            "drift_detected": drift_detected,
            "current_mean": float(current_mean),
            "baseline_mean": float(self.baseline_mean),
            "z_score": float(z_score),
            "variance_ratio": float(variance_ratio),
            "sample_size": len(current_scores)
        }
        
        if drift_detected:
            logger.warning(f"DRIFT DETECTADO: Z-score={z_score:.2f}, Variance ratio={variance_ratio:.2f}")
        
        return result
    
    def calculate_prediction_quality(self, scores: np.ndarray) -> float:
        """Calcula qualidade das predições (0-1)"""
        # Quanto maior o score máximo, melhor a confiança
        mean_score = np.mean(scores)
        return float(np.clip(mean_score, 0, 1))
