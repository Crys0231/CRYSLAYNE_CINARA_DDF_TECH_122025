"""
Componentes reutilizáveis da aplicação Streamlit
"""
from typing import Optional

from .header import render_header
from .layout import (
    get_global_css,
    render_sidebar,
    render_footer,
    render_custom_divider,
    render_metric_card
)

# Exportar tudo
__all__ = [
    'render_header',
    'render_sidebar',
    'render_input_section',
    'render_results',
    'get_global_css',
    'render_footer',
    'render_custom_divider',
    'render_metric_card',
]