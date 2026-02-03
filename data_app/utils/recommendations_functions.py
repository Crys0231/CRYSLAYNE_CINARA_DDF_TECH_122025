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
            
            # ============================================================
            # EXTRAÇÃO DE PREÇO - PRIORIDADE:
            # ============================================================
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
            
            # ============================================================
            # EXTRAÇÃO DE CAMPOS TÉCNICOS (CORRIGIDO)
            # ============================================================
            
            # max_speed (RPM)
            max_speed = product_data.get('max_speed')
            max_speed_int = int(max_speed) if pd.notna(max_speed) and max_speed > 0 else 0
            
            # load_capacity (Carga)
            load_capacity = product_data.get('load_capacity')
            load_capacity_int = int(load_capacity) if pd.notna(load_capacity) and load_capacity > 0 else 0
            
            # temperature_limit
            temperature_limit = product_data.get('temperature_limit')
            temperature_limit_int = int(temperature_limit) if pd.notna(temperature_limit) and temperature_limit > 0 else 0
            
            # unit_cost
            unit_cost = product_data.get('unit_cost')
            unit_cost_float = float(unit_cost) if pd.notna(unit_cost) and unit_cost > 0 else 0.0
            
            # ============================================================
            # MONTAR RECOMENDAÇÃO FORMATADA COM TODOS OS CAMPOS
            # ============================================================
            formatted.append({
                # Identificação
                'product_id': product_id,
                'product_name': product_data.get('product_name', 'N/A'),
                'bearing_type': product_data.get('bearing_type', 'N/A'),
                'manufacturer': product_data.get('manufacturer', 'N/A'),
                
                # Score
                'score': float(rec.get('score', 0)),
                
                # Valores financeiros
                'price': price,
                'unit_cost': unit_cost_float,
                
                # Métricas técnicas
                'max_speed': max_speed_int,
                'load_capacity': load_capacity_int,
                'temperature_limit': temperature_limit_int,
                'rpm_capacity': max_speed_int,                # (alias de max_speed)
                
                # Conteúdo
                'technical_description': product_data.get('technical_description', ''),
            })
        
        except Exception as e:
            print(f"❌ Erro ao formatar recomendação {rec.get('product_id')}: {e}")
            continue
    
    return formatted



# ============================================================
# FUNÇÃO DE VALIDAÇÃO (PARA DEBUG)
# ============================================================

def validate_formatted_recommendations(formatted_recs):
    """
    Valida se todas as recomendações formatadas têm os campos necessários.
    
    Args:
        formatted_recs (list): Lista de recomendações formatadas
        
    Returns:
        dict: Status da validação
    """
    required_fields = [
        'product_id', 'product_name', 'bearing_type',
        'score', 'price', 'unit_cost',
        'max_speed', 'load_capacity', 'temperature_limit',
        'rpm_capacity', 'technical_description'
    ]
    
    results = {
        'total': len(formatted_recs),
        'valid': 0,
        'missing_fields': {},
        'zero_values': {}
    }
    
    for rec in formatted_recs:
        is_valid = True
        
        # Verificar campos obrigatórios
        for field in required_fields:
            if field not in rec:
                is_valid = False
                results['missing_fields'][field] = results['missing_fields'].get(field, 0) + 1
        
        # Verificar valores zerados (potencial problema)
        if rec.get('max_speed', 0) == 0:
            results['zero_values']['max_speed'] = results['zero_values'].get('max_speed', 0) + 1
        
        if rec.get('load_capacity', 0) == 0:
            results['zero_values']['load_capacity'] = results['zero_values'].get('load_capacity', 0) + 1
        
        if rec.get('price', 0) == 0:
            results['zero_values']['price'] = results['zero_values'].get('price', 0) + 1
        
        if is_valid:
            results['valid'] += 1
    
    return results