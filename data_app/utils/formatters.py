"""Formatadores de dados para exibição"""
import pandas as pd
import numpy as np

def format_price(price):
    """Formata preço em R$ brasileiro"""
    if price is None or pd.isna(price):
        return "N/A"
    
    try:
        price_float = float(price)
        if price_float <= 0:
            return "N/A"
        
        # Formato brasileiro: R$ 1.234,56
        formatted = f"R$ {price_float:,.2f}"
        # Converter . , para separadores brasileiros
        formatted = formatted.replace(',', '_temp_').replace('.', ',').replace('_temp_', '.')
        return formatted
    except:
        return "N/A"

def format_percentage(value):
    """Formata percentual"""
    if value is None or pd.isna(value):
        return "N/A"
    try:
        return f"{float(value):.1%}"
    except:
        return "N/A"

def format_number(value, decimals=0):
    """Formata número inteiro"""
    if value is None or pd.isna(value):
        return "N/A"
    try:
        return f"{float(value):,.{decimals}f}"
    except:
        return "N/A"

def format_bearing_type(bearing_type):
    """Formata tipo de rolamento com emoji"""
    if bearing_type is None or pd.isna(bearing_type):
        return "⚙️ Desconhecido"
    
    emoji_map = {
        'Autocompensador': '⚙️',
        'Esférico': '⭕',
        'Cilíndrico': '🔴',
        'Contato Angular': '📐',
        'Desgate': '⚡',
    }
    
    bearing_str = str(bearing_type).strip()
    emoji = emoji_map.get(bearing_str, '⚙️')
    return f"{emoji} {bearing_str}"
