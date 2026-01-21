"""
Gerenciamento centralizado de session state
Elimina duplicação em todas as páginas
"""

import streamlit as st
from typing import Optional, Any
import sys
import os
import logging

def setup_paths() -> None:
    """
    Configura paths do projeto uma única vez.
    
    Adiciona o diretório base ao sys.path para permitir imports.
    Pode ser chamado múltiplas vezes (idempotente).
    """
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if base not in sys.path:
        sys.path.insert(0, base)
    
@st.cache_resource
def get_engine() -> Optional[Any]:
    """
    Singleton: Inicializa engine de recomendação com cache.
    
    Returns:
        RecommendationEngine se sucesso, None se falha.
        
    Note:
        Decorado com @st.cache_resource para usar uma única instância.
        Retorna None gracefully, não mata a app.
    """

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )

    try:
        from src.recommendation_engine import RecommendationEngine
        from utils.data_loader import load_products_data
        
        products_df = load_products_data()
        if products_df is None or products_df.empty:
            st.error("❌ Erro: Dados de produtos não encontrados")
            return None
        
        engine = RecommendationEngine()
        engine.fit(products_df, text_column="full_description")
        return engine
    except ImportError as e:
        st.error(f"❌ Módulo não encontrado: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Erro ao inicializar engine: {e}")
        return None

@st.cache_data
def get_data() -> Optional[Any]:
    """
    Singleton: Carrega dados de produtos com cache.
    
    Returns:
        DataFrame com dados de produtos se sucesso, None se falha.
    """
    try:
        from utils.data_loader import load_products_data
        return load_products_data()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return None



