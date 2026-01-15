"""
Utilitários e funções auxiliares
"""

from .data_loader import load_products_data, get_product_info
from .recommendations import format_recommendations
from .formatters import format_price, format_score, format_bearing_type

__all__ = [
    'load_products_data',
    'get_product_info',
    'format_recommendations',
    'format_price',
    'format_score',
    'format_bearing_type',
]
