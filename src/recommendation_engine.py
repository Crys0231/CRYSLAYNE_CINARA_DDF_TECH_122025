import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import warnings
import os
warnings.filterwarnings('ignore')

class RecommendationEngine:
    def __init__(self, max_features=1000, ngram_range=(1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            lowercase=True,
            stop_words=None,  # Suporte total ao Português
            analyzer='word'
        )
        self.products_df = None
        self.tfidf_matrix = None
        self.is_fitted = False

    def fit(self, products_df, text_column="full_description"):
        if products_df is None or products_df.empty:
            raise ValueError("DataFrame vazio")
        
        # Garante que a coluna de texto exista
        if text_column not in products_df.columns:
            cols = ['bearing_type', 'material', 'technical_description']
            available = [c for c in cols if c in products_df.columns]
            products_df[text_column] = products_df[available].astype(str).agg(' '.join, axis=1)

        self.products_df = products_df.copy()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.products_df[text_column])
        self.is_fitted = True
        return self

    def recommend(self, query, top_k=5, min_score=0.0):
        """
        Gera recomendações baseadas em uma query
        
        Args:
            query (str): Texto de busca
            top_k (int): Número máximo de resultados
            min_score (float): Score mínimo para incluir resultado (0.0 a 1.0)
        
        Returns:
            list: Lista de dicionários com recomendações
        """
        if not self.is_fitted:
            raise ValueError("O modelo precisa ser treinado primeiro.")
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Ordena por similaridade decrescente
        top_indices = np.argsort(similarities)[::-1]
        
        recommendations = []
        for idx in top_indices:
            # Para quando atingir top_k resultados válidos
            if len(recommendations) >= top_k:
                break
            
            # Filtra por score mínimo
            if similarities[idx] < min_score:
                continue
            
            row = self.products_df.iloc[idx]
            recommendations.append({
                'product_id': str(row.get('product_id', 'N/A')),
                'product_name': str(row.get('product_name', 'N/A')),
                'score': float(similarities[idx]),
                'bearing_type': str(row.get('bearing_type', 'N/A')),
                'price': float(row.get('list_price', 0)),
                'technical_description': str(row.get('technical_description', 'N/A'))
            })
        
        return recommendations

    def get_info(self):
        """Retorna metadados do modelo"""
        if not self.is_fitted:
            return {"status": "Não treinado"}
        return {
            "num_products": self.tfidf_matrix.shape[0],
            "vocab_size": len(self.vectorizer.vocabulary_),
            "params": self.vectorizer.get_params()
        }

    def save_model(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load_model(cls, path):
        return joblib.load(path)