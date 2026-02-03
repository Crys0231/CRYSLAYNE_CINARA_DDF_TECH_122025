"""
Utils Package - DDF Tech 2025
Módulo centralizado de utilitários para a aplicação
"""

# ============================================================================
# IMPORTS DE MÓDULOS INTERNOS
# ============================================================================

from .data_loader import load_products_data
from .formatters import (
    format_price,
    format_percentage,
    format_number,
    format_bearing_type
)
from .session import (
    setup_paths,
    get_engine,
    get_data
)
from .history import (
    ensure_history_exists,
    get_history_stats,
    get_queries_by_hour,
    format_history_dataframe
)
from .plotting import (
    setup_dark_figure,
    apply_dark_style,
    setup_subplots_dark,
    style_bar_chart,
    DARK_COLORS
)
from .examples import (
    load_examples,
    get_examples_by_industry,
    list_industries
)
from .logger import (
    setup_logger,
    setup_monitoring_logger,
    setup_recommendations_logger,
    setup_errors_logger,
    root_logger
)

# Importação condicional do recommendations (pode não existir em alguns contextos)
try:
    from .recommendations_functions import format_recommendations
    _HAS_RECOMMENDATIONS = True
except ImportError:
    _HAS_RECOMMENDATIONS = False
    format_recommendations = None

# ============================================================================
# METADATA
# ============================================================================

__version__ = "1.0.0"
__author__ = "Cryslayne Cinara"
__project__ = "DDF Tech 2025"

# ============================================================================
# EXPORTS PÚBLICOS
# ============================================================================

__all__ = [
    # Data Loader
    'load_products_data',
    
    # Formatters
    'format_price',
    'format_percentage',
    'format_number',
    'format_bearing_type',
    
    # Session Management
    'setup_paths',
    'get_engine',
    'get_data',
    
    # History Management
    'ensure_history_exists',
    'get_history_stats',
    'get_queries_by_hour',
    'format_history_dataframe',
    
    # Plotting
    'setup_dark_figure',
    'apply_dark_style',
    'setup_subplots_dark',
    'style_bar_chart',
    'DARK_COLORS',
    
    # Examples
    'load_examples',
    'get_examples_by_industry',
    'list_industries',
    
    # Logger
    'setup_logger',
    'setup_monitoring_logger',
    'setup_recommendations_logger',
    'setup_errors_logger',
    'root_logger',
]

# Adicionar format_recommendations apenas se disponível
if _HAS_RECOMMENDATIONS:
    __all__.append('format_recommendations')

# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA
# ============================================================================

def initialize_app():
    """
    Inicializa todos os componentes necessários da aplicação
    
    Uso:
        >>> from data_app.utils import initialize_app
        >>> engine, data = initialize_app()
    
    Returns:
        tuple: (engine, products_data)
    """
    setup_paths()
    ensure_history_exists()
    engine = get_engine()
    data = get_data()
    
    return engine, data

def get_app_info():
    """
    Retorna informações sobre a aplicação
    
    Returns:
        dict: Informações de versão e módulos disponíveis
    """
    return {
        "version": __version__,
        "author": __author__,
        "project": __project__,
        "modules": {
            "data_loader": True,
            "formatters": True,
            "session": True,
            "history": True,
            "plotting": True,
            "examples": True,
            "logger": True,
            "recommendations": _HAS_RECOMMENDATIONS
        }
    }

# ============================================================================
# INICIALIZAÇÃO DO LOGGER
# ============================================================================

# Logger é inicializado automaticamente ao importar o módulo
root_logger.info(f"Utils package inicializado - v{__version__}")
root_logger.info(f"Módulos disponíveis: {len(__all__)}")