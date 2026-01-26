import sys
import os
from pathlib import Path
import pandas as pd
import pytest

ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR / 'src'
sys.path.insert(0, str(SRC_DIR))

from recommendation_engine import RecommendationEngine


class TestRecommendationEngine:
    """Suite de testes para o RecommendationEngine"""
    
    @pytest.fixture
    def sample_data(self):
        """Cria dados de exemplo para testes"""
        return pd.DataFrame({
            'product_id': ['P001', 'P002', 'P003', 'P004'],
            'product_name': [
                'Rolamento Esférico Alta Rotação',
                'Rolamento Cilíndrico Alta Temperatura',
                'Rolamento Cônico Média Carga',
                'Rolamento Rígido Baixa Vibração'
            ],
            'bearing_type': ['Esférico', 'Cilíndrico', 'Cônico', 'Rígido'],
            'material': ['Aço Inox', 'Aço Carbono', 'Aço Liga', 'Aço Inox'],
            'technical_description': [
                'Alta rotação suporta 15000 RPM',
                'Alta temperatura até 200°C',
                'Suporta cargas radiais e axiais',
                'Baixa vibração e ruído'
            ],
            'list_price': [150.0, 200.0, 180.0, 120.0]
        })
    
    def test_engine_initialization(self):
        """Teste: Inicialização do motor"""
        engine = RecommendationEngine(max_features=100, ngram_range=(1, 2))
        
        assert engine.vectorizer is not None
        assert engine.products_df is None
        assert engine.tfidf_matrix is None
        assert engine.is_fitted == False
        print("✓ Inicialização OK")
    
    def test_fit_with_valid_data(self, sample_data):
        """Teste: Treinamento com dados válidos"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        
        assert engine.is_fitted == True
        assert engine.products_df is not None
        assert engine.tfidf_matrix is not None
        assert engine.tfidf_matrix.shape[0] == len(sample_data)
        print("✓ Fit OK")
    
    def test_fit_with_empty_dataframe(self):
        """Teste: Treinamento com DataFrame vazio"""
        engine = RecommendationEngine()
        
        with pytest.raises(ValueError, match="DataFrame vazio"):
            engine.fit(pd.DataFrame())
        print("✓ Validação DataFrame vazio OK")
    
    def test_fit_with_none(self):
        """Teste: Treinamento com None"""
        engine = RecommendationEngine()
        
        with pytest.raises(ValueError, match="DataFrame vazio"):
            engine.fit(None)
        print("✓ Validação None OK")
    
    def test_recommend_without_fit(self):
        """Teste: Recomendação sem treinamento"""
        engine = RecommendationEngine()
        
        with pytest.raises(ValueError, match="precisa ser treinado"):
            engine.recommend("teste")
        print("✓ Validação modelo não treinado OK")
    
    def test_recommend_basic(self, sample_data):
        """Teste: Recomendação básica"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        
        recommendations = engine.recommend("alta rotação", top_k=2)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 2
        assert all('product_id' in r for r in recommendations)
        assert all('score' in r for r in recommendations)
        print("✓ Recomendação básica OK")
    
    def test_recommend_with_min_score(self, sample_data):
        """Teste: Recomendação com score mínimo"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        
        recommendations = engine.recommend(
            "alta temperatura",
            top_k=5,
            min_score=0.1
        )
        
        # Todos os scores devem ser >= min_score
        assert all(r['score'] >= 0.1 for r in recommendations)
        print("✓ Filtro min_score OK")
    
    def test_recommend_no_results_with_high_min_score(self, sample_data):
        """Teste: Sem resultados com min_score muito alto"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        
        recommendations = engine.recommend(
            "produto inexistente xyz123",
            top_k=5,
            min_score=0.9
        )
        
        # Pode não retornar nada se não houver matches bons
        assert isinstance(recommendations, list)
        print("✓ Min score alto OK")
    
    def test_recommend_respects_top_k(self, sample_data):
        """Teste: Respeita o limite top_k"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        
        for k in [1, 2, 3]:
            recommendations = engine.recommend("rolamento", top_k=k)
            assert len(recommendations) <= k
        print("✓ Limite top_k OK")
    
    def test_get_info_before_fit(self):
        """Teste: Info antes do treinamento"""
        engine = RecommendationEngine()
        info = engine.get_info()
        
        assert 'status' in info
        assert info['status'] == "Não treinado"
        print("✓ Info antes do fit OK")
    
    def test_get_info_after_fit(self, sample_data):
        """Teste: Info após treinamento"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        info = engine.get_info()
        
        assert 'num_products' in info
        assert 'vocab_size' in info
        assert 'params' in info
        assert info['num_products'] == len(sample_data)
        assert info['vocab_size'] > 0
        print("✓ Info após fit OK")
    
    def test_save_and_load_model(self, sample_data, tmp_path):
        """Teste: Salvar e carregar modelo"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        
        # Salvar
        model_path = tmp_path / "test_model.pkl"
        engine.save_model(str(model_path))
        assert model_path.exists()
        
        # Carregar
        loaded_engine = RecommendationEngine.load_model(str(model_path))
        assert loaded_engine.is_fitted == True
        assert loaded_engine.products_df is not None
        
        # Testar que funciona
        recommendations = loaded_engine.recommend("alta rotação", top_k=1)
        assert len(recommendations) > 0
        print("✓ Save/Load modelo OK")
    
    def test_recommendation_structure(self, sample_data):
        """Teste: Estrutura das recomendações"""
        engine = RecommendationEngine()
        engine.fit(sample_data)
        
        recommendations = engine.recommend("temperatura", top_k=1)
        
        if len(recommendations) > 0:
            rec = recommendations[0]
            required_fields = [
                'product_id', 'product_name', 'score',
                'bearing_type', 'price', 'technical_description'
            ]
            
            for field in required_fields:
                assert field in rec, f"Campo {field} ausente"
            
            assert isinstance(rec['score'], float)
            assert 0.0 <= rec['score'] <= 1.0
            assert isinstance(rec['price'], float)
        print("✓ Estrutura recomendação OK")


def test_full_pipeline():
    """Teste de integração completo"""
    print("\n" + "="*60)
    print("TESTE DE INTEGRAÇÃO COMPLETO")
    print("="*60)
    
    # 1. Carregar os dados
    data_path = root / 'data' / 'refined' / 'products_features.parquet'
    
    if not data_path.exists():
        print(f"⚠ Base de dados não encontrada em: {data_path}")
        print("Usando dados de exemplo para teste...")
        
        # Criar dados de exemplo
        df = pd.DataFrame({
            'product_id': [f'P{i:03d}' for i in range(10)],
            'product_name': [f'Rolamento Tipo {i}' for i in range(10)],
            'bearing_type': ['Esférico'] * 10,
            'material': ['Aço Inox'] * 10,
            'technical_description': [
                f'Descrição técnica do produto {i}' for i in range(10)
            ],
            'list_price': [100.0 + i*10 for i in range(10)]
        })
    else:
        df = pd.read_parquet(data_path)
        print(f"✓ Base carregada: {len(df)} produtos")
    
    # 2. Treinamento
    engine = RecommendationEngine(max_features=1000)
    engine.fit(df)
    print(f"✓ Modelo treinado")
    
    # 3. Validação
    info = engine.get_info()
    print(f"✓ Vocabulário: {info['vocab_size']} termos")
    print(f"✓ Produtos: {info['num_products']}")
    
    # 4. Teste de busca
    test_queries = [
        "Rolamento para alta temperatura e rotação",
        "Vibração e ruído baixo",
        "Carga pesada"
    ]
    
    print("\n" + "-"*60)
    print("TESTES DE BUSCA")
    print("-"*60)
    
    for query in test_queries:
        recs = engine.recommend(query, top_k=2, min_score=0.01)
        print(f"\nQuery: '{query}'")
        print(f"Resultados: {len(recs)}")
        
        for i, rec in enumerate(recs, 1):
            print(f"  {i}. {rec['product_name'][:50]}")
            print(f"     Score: {rec['score']:.4f}")
    
    # 5. Exportação
    model_path = root / 'models' / 'recommendation_engine.pkl'
    engine.save_model(str(model_path))
    print(f"\n✓ Modelo salvo em: {model_path}")
    
    print("\n" + "="*60)
    print("INTEGRAÇÃO COMPLETA ✓")
    print("="*60)


if __name__ == "__main__":
    # Rodar testes unitários
    print("Executando testes unitários...")
    pytest.main([__file__, '-v', '-s', '-k', 'Test'])
    
    # Rodar teste de integração
    print("\n\nExecutando teste de integração...")
    test_full_pipeline()