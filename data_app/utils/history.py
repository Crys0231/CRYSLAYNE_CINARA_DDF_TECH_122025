import streamlit as st
from typing import Dict, List, Tuple
from datetime import datetime
import pandas as pd
import re


def ensure_history_exists() -> List[dict]:
    """Garante que histórico existe no session state"""
    import streamlit as st
    if 'history' not in st.session_state:
        st.session_state.history = []
    return st.session_state.history


def get_history_stats(history: List[dict]) -> Dict:
    """
    Calcula estatísticas do histórico - VERSÃO CORRIGIDA
    Usado em: analytics.py, monitoring.py
    """
    if not history or len(history) == 0:
        return {
            'total_queries': 0,
            'total_results': 0,
            'avg_results': 0,
            'queries_by_hour': {},
            'word_frequency': {}
        }

    total_queries = len(history)
    total_results = sum(item.get('count', 0) for item in history)
    avg_results = total_results / total_queries if total_queries > 0 else 0

    # Agrupar por hora
    queries_by_hour = {}
    for item in history:
        timestamp = item.get('timestamp')
        hour = _extract_hour(timestamp)
        if hour is not None:
            queries_by_hour[hour] = queries_by_hour.get(hour, 0) + 1

    # Frequência de palavras
    word_freq = _calculate_word_frequency(history)

    return {
        'total_queries': total_queries,
        'total_results': total_results,
        'avg_results': avg_results,
        'queries_by_hour': queries_by_hour,
        'word_frequency': word_freq
    }


def _extract_hour(timestamp) -> int | None:
    """
    Extrai hora do timestamp (datetime ou string)
    """
    
    if timestamp is None:
        return None
    
    # Se já é datetime object (melhor caso)
    if isinstance(timestamp, datetime):
        try:
            return timestamp.hour
        except Exception:
            return None
    
    # Se é string, tenta vários formatos
    if isinstance(timestamp, str):
        if not timestamp or timestamp.strip() == '':
            return None
        
        timestamp = timestamp.strip()
        
        # Lista expandida de formatos para tentar
        formats = [
            # Brasileiros
            '%d/%m %H:%M',
            '%d/%m %H:%M:%S',
            '%d/%m/%Y %H:%M',
            '%d/%m/%Y %H:%M:%S',
            
            # ISO (internacionais)
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M',
            
            # Outros
            '%d-%m-%Y %H:%M:%S',
            '%d-%m-%Y %H:%M',
            '%d/%m/%Y - %H:%M:%S',
            '%d/%m/%Y - %H:%M',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(timestamp, fmt)
                return dt.hour
            except ValueError:
                continue
            except Exception:
                continue
        
        # Se nenhum formato funcionou, tenta extrair hora manualmente
        try:
            if ':' in timestamp:
                # Procura por padrão HH:MM ou HH:MM:SS
                match = re.search(r'(\d{1,2}):(\d{2})', timestamp)
                if match:
                    hour = int(match.group(1))
                    if 0 <= hour <= 23:
                        return hour
        except Exception:
            pass
        
        return None
    
    return None


def _calculate_word_frequency(history: List[dict]) -> Dict[str, int]:
    """
    Calcula frequência de palavras-chave nas consultas
    """
    
    if not history or len(history) == 0:
        return {}
    
    # Juntar todas as queries
    all_text = ' '.join(str(item.get('query', '')) for item in history if item.get('query'))
    
    if not all_text or all_text.strip() == '':
        return {}
    
    # Dividir em palavras e converter para minúsculas
    words = all_text.lower().split()
    
    # Stop words MÍNIMAS (só as mais comuns)
    stop_words = {
        'de', 'da', 'do', 'dos', 'das',
        'em', 'na', 'no', 'nas', 'nos',
        'o', 'a', 'os', 'as',
        'e', 'ou',
        'para', 'por',
        'com', 'sem'
    }
    
    # Aceita palavras com 3+ caracteres (não > 3)
    # Aceita alfanuméricos (para "10000rpm", "6000", etc)
    filtered = []
    for w in words:
        # Remove pontuação das extremidades
        w_clean = w.strip('.,;:!?()[]{}')
        
        # Filtra: >= 3 caracteres, não é stop word, tem pelo menos uma letra
        if len(w_clean) >= 3 and w_clean not in stop_words and any(c.isalpha() for c in w_clean):
            filtered.append(w_clean)
    
    if not filtered:
        return {}
    
    # Contar frequências
    freq = {}
    for word in filtered:
        freq[word] = freq.get(word, 0) + 1
    
    # Retorna apenas se houver frequências
    return freq if freq else {}


def get_queries_by_hour(history: List[dict]) -> Dict[int, int]:
    """Agrupa consultas por hora do dia"""
    
    if not history or len(history) == 0:
        return {}
    
    hour_counts = {}
    for item in history:
        hour = _extract_hour(item.get('timestamp'))
        if hour is not None:
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    return hour_counts if hour_counts else {}


def format_history_dataframe(history: List[dict]) -> pd.DataFrame:
    """Formata histórico como DataFrame para exibição"""
    
    if not history or len(history) == 0:
        return pd.DataFrame(columns=['ID', 'Horário', 'Consulta', 'Resultados'])
    
    history_data = []
    for i, item in enumerate(reversed(history), 1):
        timestamp = item.get('timestamp')
        time_str = _format_timestamp(timestamp)
        query = str(item.get('query', 'N/A'))
        history_data.append({
            'ID': i,
            'Horário': time_str,
            'Consulta': query[:50] + ('...' if len(query) > 50 else ''),
            'Resultados': item.get('count', 0)
        })
    
    return pd.DataFrame(history_data)


def _format_timestamp(timestamp) -> str:
    """Formata timestamp para exibição"""
    
    if timestamp is None:
        return 'N/A'
    
    if isinstance(timestamp, datetime):
        return timestamp.strftime('%d/%m %H:%M:%S')
    elif isinstance(timestamp, str):
        return timestamp
    
    return 'N/A'