"""
Carregador centralizado de exemplos por indústria
Centraliza lógica de leitura do examples.json
"""
import json
import os
from pathlib import Path
from typing import Dict

def get_config_path(filename: str) -> str:
    """
    Encontra caminho do arquivo de configuração
    
    Args:
        filename: Nome do arquivo (ex: 'examples.json')
    
    Returns:
        Caminho completo do arquivo
    """
    possible_paths = [
        f'data_app/config/{filename}',
        f'./data_app/config/{filename}',
        f'../data_app/config/{filename}',
        Path(__file__).parent.parent / 'config' / filename,
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return str(path)
    
    # Fallback: retorna o primeiro caminho (para mensagem de erro clara)
    return f'data_app/config/{filename}'

def load_examples() -> Dict:
    """
    Carrega exemplos por indústria do JSON
    
    Returns:
        Dict com exemplos estruturados por indústria
    
    Raises:
        FileNotFoundError: Se examples.json não for encontrado
        json.JSONDecodeError: Se JSON estiver malformado
    
    Example:
        >>> examples = load_examples()
        >>> industries = list(examples.keys())
        >>> print(industries[0])  # '🏭 Siderurgia'
    """
    config_path = get_config_path('examples.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            examples = json.load(f)
        
        # Validar estrutura básica
        if not isinstance(examples, dict):
            raise ValueError("examples.json deve ser um objeto JSON")
        
        # Validar cada indústria
        for industry, data in examples.items():
            if 'principal_problema' not in data:
                raise ValueError(f"Indústria '{industry}' sem 'principal_problema'")
            if 'exemplos' not in data:
                raise ValueError(f"Indústria '{industry}' sem 'exemplos'")
            if not isinstance(data['exemplos'], list):
                raise ValueError(f"'exemplos' de '{industry}' deve ser uma lista")
        
        return examples
    
    except FileNotFoundError:
        raise FileNotFoundError(
            f"❌ Arquivo não encontrado: {config_path}\n"
            f"💡 Certifique-se de que examples.json existe em data_app/config/"
        )
    
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"❌ Erro ao ler JSON: {e.msg}",
            e.doc,
            e.pos
        )

def get_examples_by_industry(industry: str = None) -> Dict:
    """
    Retorna exemplos de uma indústria específica
    
    Args:
        industry: Nome da indústria (ex: '🏭 Siderurgia')
                 Se None, retorna todas
    
    Returns:
        Dict com exemplos da indústria ou todas
    
    Example:
        >>> examples = get_examples_by_industry('🏭 Siderurgia')
        >>> print(examples['principal_problema'])  # 'Vibração'
    """
    all_examples = load_examples()
    
    if industry is None:
        return all_examples
    
    if industry not in all_examples:
        raise KeyError(f"Indústria '{industry}' não encontrada. "
                      f"Disponíveis: {list(all_examples.keys())}")
    
    return all_examples[industry]

def list_industries() -> list:
    """
    Lista todas as indústrias disponíveis
    
    Returns:
        Lista de nomes de indústrias
    
    Example:
        >>> industries = list_industries()
        >>> print(len(industries))  # 7
    """
    examples = load_examples()
    return list(examples.keys())