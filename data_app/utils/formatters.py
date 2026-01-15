"""
Funções de formatação para exibição de dados
"""

def format_price(price):
    """Formata preço em formato brasileiro"""
    if price is None or price == 0:
        return "N/A"
    return f"R$ {price:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

def format_score(score):
    """Formata score de similaridade"""
    if score is None:
        return "N/A"
    
    if score > 0.5:
        return f"🟢 {score:.1%}"
    elif score > 0.3:
        return f"🟡 {score:.1%}"
    else:
        return f"🔴 {score:.1%}"

def format_bearing_type(bearing_type):
    """Formata tipo de rolamento com emoji"""
    emoji_map = {
        'Autocompensador': '⚙️',
        'Esférico': '⭕',
        'Cilíndrico': '🔴',
        'Contato Angular': '📐',
        'Agujas': '📍',
    }
    return f"{emoji_map.get(bearing_type, '⚙️')} {bearing_type}"

def format_description(desc, max_length=100):
    """Trunca descrição para tamanho máximo"""
    if desc is None:
        return "N/A"
    if len(desc) > max_length:
        return desc[:max_length] + "..."
    return desc

def format_industry(industry):
    """Formata indústria com emoji"""
    emoji_map = {
        'Siderurgia': '🏭',
        'Alimentos': '🍱',
        'Mineração': '⛏️',
        'Energia': '⚡',
        'Automotiva': '🚗',
        'Papel e Celulose': '📄',
        'Química': '⚗️',
        'Cimento': '🏗️',
    }
    return f"{emoji_map.get(industry, '🏢')} {industry}"
