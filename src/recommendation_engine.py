"""
RecommendationEngine - Motor de recomendação TF-IDF para rolamentos
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class RecommendationEngine:
    """Engine de recomendação usando TF-IDF"""
    
    def __init__(self, max_features=500, ngram_range=(1, 2)):
        """
        Inicializar engine
        
        Args:
            max_features: Número máximo de features TF-IDF
            ngram_range: Range de n-gramas
        """
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            lowercase=True,
            stop_words='english',
            analyzer='char'
        )
        self.products_df = None
        self.tfidf_matrix = None
        self.is_fitted = False
        print("✅ RecommendationEngine inicializado")
    
    def fit(self, products_df, text_column="full_description"):
        """
        Treinar o engine com dados de produtos
        
        Args:
            products_df: DataFrame com produtos
            text_column: Coluna contendo descrições técnicas
        """
        if products_df is None or products_df.empty:
            raise ValueError("❌ DataFrame vazio")
        
        # Validar coluna
        if text_column not in products_df.columns:
            print(f"⚠️ Coluna '{text_column}' não encontrada")
            print(f"📋 Colunas disponíveis: {products_df.columns.tolist()}")
            # Usar a primeira coluna de texto disponível
            text_column = "product_name"
        
        self.products_df = products_df.copy()
        
        # Validar e completar coluna de texto
        if text_column in self.products_df.columns:
            # Preencher vazios com nome do produto
            self.products_df[text_column] = self.products_df[text_column].fillna(
                self.products_df['product_name']
            )
        else:
            self.products_df[text_column] = self.products_df['product_name']
        
        # Converter para string
        descriptions = self.products_df[text_column].astype(str).values
        
        # Treinar TF-IDF
        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(descriptions)
            self.is_fitted = True
            print(f"✅ Engine treinado com {len(self.products_df)} produtos")
            return True
        except Exception as e:
            print(f"❌ Erro ao treinar: {e}")
            raise
    
    def recommend(self, query, top_k=10):
        """
        Gerar recomendações para uma query
        
        Args:
            query: Descrição do problema/necessidade
            top_k: Número de recomendações
        
        Returns:
            list: Recomendações ordenadas por score
        """
        if not self.is_fitted:
            raise ValueError("❌ Engine não foi treinado. Use .fit() primeiro")
        
        if not query or not isinstance(query, str):
            raise ValueError("❌ Query inválida")
        
        try:
            # Vetorizar query
            query_vector = self.vectorizer.transform([query])
            
            # Calcular similaridade
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Top K
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            # Formatar resultados
            recommendations = []
            for idx in top_indices:
                if similarities[idx] > 0:  # Apenas scores positivos
                    row = self.products_df.iloc[idx]
                    recommendations.append({
                        'product_id': str(row.get('product_id', 'N/A')),
                        'product_name': str(row.get('product_name', 'N/A')),
                        'bearing_type': str(row.get('bearing_type', 'N/A')),
                        'score': float(similarities[idx]),
                        'price': float(row.get('list_price', row.get('unit_cost', 0))),
                        'rpm_capacity': int(row.get('max_speed', 0)),
                        'technical_description': str(row.get('technical_description', 'N/A'))[:200],
                        'unit_cost': float(row.get('unit_cost', 0)),
                        'load_capacity': float(row.get('load_capacity', 0)),
                    })
            
            print(f"✅ {len(recommendations)} recomendações geradas (score min: {min([r['score'] for r in recommendations]):.4f})")
            return recommendations
        
        except Exception as e:
            print(f"❌ Erro ao gerar recomendações: {e}")
            raise
