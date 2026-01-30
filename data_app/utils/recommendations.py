"""Formatador de recomendações com extração de preços"""
import pandas as pd

def format_recommendations(recommendations, products_df):
    """
    Formata recomendações da engine para exibição    
    Args:
        recommendations (list): Lista de dicts com recomendações da engine
        products_df (DataFrame): DataFrame com dados dos produtos
    
    Returns:
        list: Lista de dicts formatados
    """
    
    if not recommendations or products_df is None or products_df.empty:
        return []
    
    formatted = []
    
    for rec in recommendations:
        try:
            product_id = rec.get('product_id')
            
            if not product_id:
                continue
            
            # Buscar dados do produto
            product_row = products_df[products_df['product_id'] == product_id]
            
            if product_row.empty:
                print(f"⚠️ Produto {product_id} não encontrado no DataFrame")
                continue
            
            # Extrair dados
            product_data = product_row.iloc[0].to_dict()
            
            # EXTRAÇÃO DE PREÇO - PRIORIDADE:
            # 1. list_price (preço de venda)
            # 2. unit_cost (custo unitário como fallback)
            price = 0
            if 'list_price' in product_data:
                price_val = product_data.get('list_price')
                if pd.notna(price_val) and price_val > 0:
                    price = float(price_val)
            
            # Se list_price está vazio/nulo, usar unit_cost
            if price == 0 and 'unit_cost' in product_data:
                price_val = product_data.get('unit_cost')
                if pd.notna(price_val) and price_val > 0:
                    price = float(price_val)
            
            # Montar recomendação formatada
            max_speed = product_data.get('max_speed', 0) or product_data.get('rpm_capacity', 0)
            rpm_capacity = int(max_speed) if max_speed else 0

            formatted.append({
                'product_id': product_id,
                'product_name': product_data.get('product_name', 'N/A'),
                'bearing_type': product_data.get('bearing_type', 'N/A'),
                
                # Valores financeiros
                'price': price,
                'unit_cost': float(product_data.get('unit_cost', 0)),

                # Métricas técnicas (NOMES CORRETOS)
                'max_speed': int(product_data.get('max_speed', 0)),
                'load_capacity': int(product_data.get('load_capacity', 0)),
                'temperature_limit': int(product_data.get('temperature_limit', 0)),

                # Conteúdo
                'technical_description': product_data.get('technical_description', ''),
                'score': float(rec.get('score', 0)),
            })
        
        except Exception as e:
            print(f"❌ Erro ao formatar recomendação {rec.get('product_id')}: {e}")
            continue
    
    return formatted
