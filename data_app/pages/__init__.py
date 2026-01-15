"""
Páginas multi-página da aplicação Streamlit
"""

# Páginas são importadas automaticamente pelo Streamlit
# Este arquivo apenas permite importações diretas se necessário

from . import home
from . import recommendations
from . import analytics
from . import about

__all__ = ['home', 'recommendations', 'analytics', 'about']
