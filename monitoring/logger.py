"""
Sistema de Logging - DDF Tech 2025
Configuração centralizada de logs
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str, log_dir: str = "logs") -> logging.Logger:
    """
    Configura logger com formato padronizado
    
    Args:
        name: Nome do logger
        log_dir: Diretório para arquivos de log
        
    Returns:
        Logger configurado
    """
    # Criar diretório se não existir
    Path(log_dir).mkdir(exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Formato dos logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo
    log_file = Path(log_dir) / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Logger global para monitoramento
monitoring_logger = setup_logger("monitoring")