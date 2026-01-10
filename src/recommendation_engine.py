# src/recommendation_engine.py

import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationEngine:
    """
    Motor de recomendação baseado em similaridade TF-IDF.
    Recomenda rolamentos (produtos) baseado em descrição de problema do cliente.
    """
    
    def __init__(self, random_state: int = 42):
        """
        Inicializar engine.
        
        Args:
            random_state: Seed para reproduzibilidade
        """
        self.vectorizer = None
        self.product_matrix = None
        self.products = None
        self.random_state = random_state
        
    def fit(self, products_df, text_column: str = 'full_description') -> 'RecommendationEngine':
        """
        Treinar vectorizer com corpus de produtos.
        
        Args:
            products_df: DataFrame com produtos
            text_column: Coluna a usar (default 'full_description')
            
        Returns:
            Self (para chaining)
        """
        self.products = products_df.copy()
        

        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            lowercase=True,
            min_df=2,
            max_df=0.8
        )
        # Fit e transformar
        self.product_matrix = self.vectorizer.fit_transform(
            self.products[text_column].fillna('')
        )
        
        return self
    
    def recommend(self, query: str, top_k: int = 5, min_score: float = 0.0) -> List[Dict]:
        """
        Recomendar top-k produtos para uma consulta.
        
        Args:
            query: String descrevendo o problema/necessidade
            top_k: Quantos produtos retornar
            min_score: Score mínimo de similaridade (0-1)
            
        Returns:
            Lista de dicts com {product_id, product_name, score}
        """
        if self.vectorizer is None or self.product_matrix is None:
            raise ValueError("Engine não foi treinado. Chame fit() primeiro.")
        
        # Transformar query
        query_vector = self.vectorizer.transform([query])
        
        # Calcular similaridade
        similarities = cosine_similarity(query_vector, self.product_matrix)[0]
        
        # Top K com filtro
        indices = np.argsort(-similarities)[:top_k]
        results = []
        
        for idx in indices:
            score = float(similarities[idx])
            if score >= min_score:
                results.append({
                    'product_id': str(self.products.iloc[idx]['product_id']),
                    'product_name': str(self.products.iloc[idx]['product_name']),
                    'score': score
                })
        
        return results
    
    def batch_recommend(self, queries: List[str], top_k: int = 5) -> Dict[str, List[Dict]]:
        """
        Recomendar para múltiplas consultas em batch.
        
        Args:
            queries: Lista de queries
            top_k: Quantos produtos por query
            
        Returns:
            Dict com {query: [recomendações]}
        """
        return {
            query: self.recommend(query, top_k)
            for query in queries
        }
    
    def save_model(self, path: str) -> None:
        """
        Salvar modelo treinado.
        
        Args:
            path: Caminho para salvar .pkl
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load_model(path: str) -> 'RecommendationEngine':
        """
        Carregar modelo treinado.
        
        Args:
            path: Caminho do arquivo .pkl
            
        Returns:
            Instância RecommendationEngine
        """
        with open(path, 'rb') as f:
            return pickle.load(f)
    
    def get_info(self) -> Dict:
        """
        Retornar informações sobre o modelo.
        
        Returns:
            Dict com metadata
        """
        return {
            'status': 'trained' if self.vectorizer else 'untrained',
            'num_products': len(self.products) if self.products is not None else 0,
            'vocab_size': len(self.vectorizer.vocabulary_) if self.vectorizer else 0,
            'tfidf_params': {
                'max_features': 1000,
                'stop_words': 'portuguese',
                'min_df': 2,
                'max_df': 0.8
            }
        }
