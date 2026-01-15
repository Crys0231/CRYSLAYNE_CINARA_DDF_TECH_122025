import pandas as pd

def format_recommendations(raw_recs, products_df):
    """Formata recomendações para exibição"""
    
    formatted = []
    
    for product_id, score in raw_recs:
        try:
            product = products_df[products_df['product_id'] == product_id].iloc
            
            formatted.append({
                'product_id': product_id,
                'product_name': product.get('product_name', 'N/A'),
                'bearing_type': product.get('bearing_type', 'N/A'),
                'price': product.get('list_price', 0),
                'score': score,
                'technical_description': product.get('technical_description', ''),
                'rpm_capacity': product.get('rpm_capacity', 0),
            })
        except Exception as e:
            print(f"Erro ao formatar recomendação: {e}")
    
    return formatted
