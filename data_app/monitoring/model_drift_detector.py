"""
Detector de Model Drift - Data Driven Bearings
Identifica quando modelo está degradando
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any

from utils.logger import setup_logger

logger = setup_logger("model_drift", log_file="logs/model_drift.log")


class DriftDetector:
    """Detecta degradação de performance (Model Drift)"""
    
    def __init__(self, window_size: int = 100):
        """
        Inicializa detector de drift
        
        Args:
            window_size: Tamanho da janela de observação
        """
        self.window_size = window_size
        self.prediction_scores = []
        self.baseline_mean = None
        self.baseline_std = None
        
        logger.info(f"DriftDetector inicializado com window_size={window_size}")
    
    def set_baseline(self, baseline_scores: np.ndarray) -> None:
        """
        Define baseline de scores históricos
        
        Args:
            baseline_scores: Array com scores históricos para baseline
        """
        if len(baseline_scores) == 0:
            logger.warning("⚠️ Tentativa de definir baseline com array vazio")
            return
        
        self.baseline_mean = np.mean(baseline_scores)
        self.baseline_std = np.std(baseline_scores)
        
        logger.info(
            f"Baseline estabelecido: "
            f"mean={self.baseline_mean:.3f}, "
            f"std={self.baseline_std:.3f}, "
            f"samples={len(baseline_scores)}"
        )
    
    def add_score(self, score: float) -> None:
        """
        Adiciona novo score à janela deslizante
        
        Args:
            score: Score de predição (0.0 a 1.0)
        """
        self.prediction_scores.append(score)
        
        # Manter apenas os últimos N scores
        if len(self.prediction_scores) > self.window_size:
            self.prediction_scores.pop(0)
        
        logger.debug(f"Score adicionado: {score:.3f} (total: {len(self.prediction_scores)})")

    def detect_drift(self) -> Dict[str, Any]:
        """
        Detecta se há drift estatístico
        
        Returns:
            Dict com informações sobre detecção de drift:
            - drift_detected: bool
            - current_mean: média atual
            - baseline_mean: média do baseline
            - z_score: desvio estatístico
            - variance_ratio: razão de variâncias
            - sample_size: tamanho da amostra
            - reason: motivo (se aplicável)
        """
        try:
            # Validação de dados suficientes
            if len(self.prediction_scores) < 10:
                logger.debug("Dados insuficientes para detecção de drift (< 10 amostras)")
                return {
                    "drift_detected": False,
                    "reason": "Dados insuficientes (< 10 amostras)",
                    "sample_size": len(self.prediction_scores)
                }
            
            if self.baseline_mean is None:
                logger.warning("Baseline não definido. Chamando set_baseline() primeiro.")
                return {
                    "drift_detected": False,
                    "reason": "Baseline não definido",
                    "sample_size": len(self.prediction_scores)
                }
            
            # Calcular estatísticas atuais
            current_scores = np.array(self.prediction_scores)
            current_mean = np.mean(current_scores)
            current_std = np.std(current_scores)
            
            # Teste 1: Mudança na média (Z-score)
            # Z > 2.0 indica mudança estatisticamente significativa (95% confiança)
            z_score = abs(current_mean - self.baseline_mean) / (self.baseline_std + 1e-6)
            
            # Teste 2: Mudança na variância
            # Ratio > 2.0 indica aumento significativo na variabilidade
            variance_ratio = current_std / (self.baseline_std + 1e-6)
            
            # Detecção de drift
            drift_detected = z_score > 2.0 or variance_ratio > 2.0
            
            result = {
                "drift_detected": drift_detected,
                "current_mean": float(current_mean),
                "baseline_mean": float(self.baseline_mean),
                "current_std": float(current_std),
                "baseline_std": float(self.baseline_std),
                "z_score": float(z_score),
                "variance_ratio": float(variance_ratio),
                "sample_size": len(current_scores)
            }
            
            # Logging detalhado
            if drift_detected:
                logger.warning(
                    f"🚨 DRIFT DETECTADO! "
                    f"Z-score={z_score:.2f} (threshold=2.0), "
                    f"Variance ratio={variance_ratio:.2f} (threshold=2.0), "
                    f"Current mean={current_mean:.3f}, "
                    f"Baseline mean={self.baseline_mean:.3f}"
                )
                result["reason"] = self._get_drift_reason(z_score, variance_ratio)
            else:
                logger.debug(
                    f"Sem drift detectado. "
                    f"Z-score={z_score:.2f}, "
                    f"Variance ratio={variance_ratio:.2f}"
                )
            
            return result
        
        except Exception as e:
            logger.error(f"Erro na detecção de drift: {e}", exc_info=True)
            return {
                "drift_detected": False,
                "reason": f"Erro: {str(e)}",
                "error": True
            }
    
    def _get_drift_reason(self, z_score: float, variance_ratio: float) -> str:
        """
        Determina a razão do drift detectado
        
        Args:
            z_score: Z-score calculado
            variance_ratio: Razão de variâncias
        
        Returns:
            Descrição da razão do drift
        """
        reasons = []
        
        if z_score > 2.0:
            direction = "aumentou" if z_score > 0 else "diminuiu"
            reasons.append(f"Média {direction} significativamente (Z={z_score:.2f})")
        
        if variance_ratio > 2.0:
            reasons.append(f"Variabilidade aumentou (ratio={variance_ratio:.2f})")
        
        return " | ".join(reasons) if reasons else "Drift detectado"
    
    def calculate_prediction_quality(self, scores: np.ndarray) -> float:
        """
        Calcula qualidade das predições (0-1)
        
        Args:
            scores: Array de scores de predições
        
        Returns:
            Score de qualidade normalizado entre 0 e 1
        """
        if len(scores) == 0:
            logger.warning("Array vazio fornecido para cálculo de qualidade")
            return 0.0
        
        # Quanto maior o score médio, melhor a confiança
        mean_score = np.mean(scores)
        quality = float(np.clip(mean_score, 0, 1))
        
        logger.debug(f"Qualidade calculada: {quality:.3f} (de {len(scores)} predições)")
        
        return quality
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas atuais do detector
        
        Returns:
            Dict com estatísticas completas
        """
        if len(self.prediction_scores) == 0:
            return {
                "sample_size": 0,
                "baseline_defined": self.baseline_mean is not None
            }
        
        current_scores = np.array(self.prediction_scores)
        
        return {
            "sample_size": len(self.prediction_scores),
            "current_mean": float(np.mean(current_scores)),
            "current_std": float(np.std(current_scores)),
            "current_min": float(np.min(current_scores)),
            "current_max": float(np.max(current_scores)),
            "baseline_mean": float(self.baseline_mean) if self.baseline_mean else None,
            "baseline_std": float(self.baseline_std) if self.baseline_std else None,
            "baseline_defined": self.baseline_mean is not None,
            "window_size": self.window_size
        }
    
    def reset(self) -> None:
        """Reseta o detector (mantém baseline)"""
        self.prediction_scores = []
        logger.info("Detector resetado (baseline mantido)")
    
    def reset_all(self) -> None:
        """Reseta tudo, incluindo baseline"""
        self.prediction_scores = []
        self.baseline_mean = None
        self.baseline_std = None
        logger.info("Detector completamente resetado (baseline removido)")