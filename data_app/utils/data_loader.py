"""
Carregador de dados com validação completa de preços
"""
import pandas as pd
import os
import numpy as np
from pathlib import Path

def get_data_path(filename):
    """Encontrar caminho do arquivo de dados"""
    # Tentar múltiplos caminhos
    possible_paths = [
        f'./data/refined/{filename}',
        f'../data/refined/{filename}',
        f'../../data/refined/{filename}',
        Path.home() / 'data' / 'refined' / filename,
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Encontrado: {path}")
            return path
    
    # Se não encontrar, retornar o padrão
    return f'./data/refined/{filename}'

def load_products_data():
    """
    Carrega dados de produtos com validação de preços
    
    Returns:
        DataFrame com produtos
    """
    try:
        path = get_data_path('dim_products.parquet')
        
        if not os.path.exists(path):
            print(f"Arquivo não encontrado: {path}")
            print("Criando DataFrame de exemplo...")
            return create_sample_products()
        
        df = pd.read_parquet(path)
        print(f"{len(df)} produtos carregados")
        
        # VALIDAÇÃO E PREENCHIMENTO DE PREÇOS
        if 'list_price' not in df.columns:
            print("Coluna 'list_price' não encontrada")
            if 'unit_cost' in df.columns:
                df['list_price'] = df['unit_cost']
                print("Usando 'unit_cost' como 'list_price'")
            else:
                df['list_price'] = 0
        
        # Validar valores
        df['list_price'] = pd.to_numeric(df['list_price'], errors='coerce').fillna(0)
        
        # Se list_price for 0 ou NaN, usar unit_cost
        if 'unit_cost' in df.columns:
            df['unit_cost'] = pd.to_numeric(df['unit_cost'], errors='coerce').fillna(0)
            mask = (df['list_price'] == 0) | (df['list_price'].isna())
            df.loc[mask, 'list_price'] = df.loc[mask, 'unit_cost']
        
        # Validar outras colunas importantes
        required_cols = {
            'product_name': 'Produto Desconhecido',
            'bearing_type': 'Tipo Desconhecido',
            'technical_description': 'Sem descrição',
            'max_speed': 0,
            'load_capacity': 0,
            'unit_cost': 0,
        }
        
        for col, default in required_cols.items():
            if col not in df.columns:
                df[col] = default
                print(f"Coluna '{col}' criada com valor padrão")
        
        # Criar full_description para a engine
        if 'full_description' not in df.columns:
            df['full_description'] = (
                df['product_name'].astype(str) + " " +
                df['bearing_type'].astype(str) + " " +
                df['technical_description'].astype(str)
            )
        
        # Estatísticas
        print(f"Preços válidos: {(df['list_price'] > 0).sum()}")
        print(f"Preço médio: R$ {df['list_price'].mean():,.2f}")
        print(f"Preço máximo: R$ {df['list_price'].max():,.2f}")

        return df
    
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return create_sample_products()

def create_sample_products():
    """Criar DataFrame de exemplo para testes"""
    data = [
        {
            'product_id': 'P00001',
            'product_name': 'Rolamento Industrial 1',
            'bearing_type': 'Autocompensador',
            'technical_description': 'Rolamento de alta precisão para aplicações de vibração',
            'max_speed': 13066,
            'load_capacity': 11548.93,
            'unit_cost': 315.72,
            'list_price': 394.65,
        },
        {
            'product_id': 'P00002',
            'product_name': 'Rolamento Industrial 2',
            'bearing_type': 'Cilíndrico',
            'technical_description': 'Rolamento cilíndrico para contaminação',
            'max_speed': 12731,
            'load_capacity': 28281.63,
            'unit_cost': 149.2,
            'list_price': 1849.94,
        },
        {
            'product_id': 'P00003',
            'product_name': 'Rolamento Industrial 3',
            'bearing_type': 'Contato Angular',
            'technical_description': 'Rolamento para alta temperatura',
            'max_speed': 10000,
            'load_capacity': 15000,
            'unit_cost': 200,
            'list_price': 500,
        },
    ]
    return pd.DataFrame(data)
