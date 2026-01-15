import pandas as pd
import os

def load_products_data():
    """Carrega dados de produtos"""
    
    try:
        # Tentar carregar do caminho relativo
        path = './data/refined/dim_products.parquet'
        
        if os.path.exists(path):
            df = pd.read_parquet(path)
            return df
        else:
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def get_product_info(product_id, products_df):
    """Obtem informações de um produto específico"""
    
    try:
        product = products_df[products_df['product_id'] == product_id].iloc
        return product.to_dict()
    except Exception as e:
        print(f"Erro ao obter info do produto: {e}")
        return None
