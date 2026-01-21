"""
Logger centralizado para o projeto.
Configuração única que pode ser usada em todos os módulos.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Criar diretório de logs se não existir
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configurar caminho do arquivo de log
LOG_FILE = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
MONITORING_LOG = LOGS_DIR / "monitoring.log"
RECOMMENDATIONS_LOG = LOGS_DIR / "recommendations.log"
ERRORS_LOG = LOGS_DIR / "errors.log"


def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """
    Configura um logger para um módulo específico.
    
    Args:
        name: Nome do módulo (geralmente __name__)
        log_file: Arquivo de log específico (opcional)
        level: Nível de logging (padrão: INFO)
        
    Returns:
        logging.Logger: Logger configurado
        
    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Iniciando aplicação")
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Configurar nível
    logger.setLevel(level)
    
    # Formato de log
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    if log_file is None:
        log_file = LOG_FILE
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def setup_monitoring_logger():
    """
    Configura logger específico para monitoramento.
    
    Returns:
        logging.Logger: Logger para monitoramento
    """
    return setup_logger("monitoring", str(MONITORING_LOG), logging.INFO)


def setup_recommendations_logger():
    """
    Configura logger específico para recomendações.
    
    Returns:
        logging.Logger: Logger para recomendações
    """
    return setup_logger("recommendations", str(RECOMMENDATIONS_LOG), logging.INFO)


def setup_errors_logger():
    """
    Configura logger específico para erros.
    
    Returns:
        logging.Logger: Logger para erros
    """
    return setup_logger("errors", str(ERRORS_LOG), logging.ERROR)


# Logger global padrão
root_logger = setup_logger("data_app", str(LOG_FILE), logging.INFO)

root_logger.info("=" * 70)
root_logger.info("🚀 APLICAÇÃO INICIADA")
root_logger.info(f"📁 Diretório de logs: {LOGS_DIR.absolute()}")
root_logger.info(f"📄 Arquivo principal: {LOG_FILE}")
root_logger.info("=" * 70)