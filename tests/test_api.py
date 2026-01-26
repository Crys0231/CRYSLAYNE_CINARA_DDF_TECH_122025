import sys 
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
import json

# sys.path.insert(0, os.path.abspath('../src'))
ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR / 'src'
sys.path.insert(0, str(SRC_DIR))

from api import app


@pytest.fixture
def client():
    """Cliente Flask para testes"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_engine():
    """Mock do RecommendationEngine"""
    engine = MagicMock()
    engine.recommend.return_value = [
        {
            'product_id': 'TEST001',
            'product_name': 'Rolamento Teste',
            'score': 0.95,
            'bearing_type': 'Esférico',
            'price': 150.00,
            'technical_description': 'Rolamento de teste para validação'
        }
    ]
    return engine


class TestAPIHealth:
    """Testes de health check"""
    
    def test_health_endpoint(self, client):
        """Teste: Health check retorna status correto"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'model_loaded' in data
        assert 'timestamp' in data
        print("✓ Health check OK")


class TestAPIMetadata:
    """Testes de metadata"""
    
    @patch('api.metadata', {'num_products': 100, 'version': '1.0'})
    def test_metadata_available(self, client):
        """Teste: Metadata disponível"""
        response = client.get('/api/v1/metadata')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'num_products' in data
        print("✓ Metadata OK")
    
    @patch('api.metadata', {})
    def test_metadata_unavailable(self, client):
        """Teste: Metadata não disponível"""
        response = client.get('/api/v1/metadata')
        assert response.status_code == 503
        
        data = json.loads(response.data)
        assert 'error' in data
        print("✓ Validação metadata vazia OK")


class TestAPIRecommend:
    """Testes de recomendação única"""
    
    @patch('api.engine', None)
    def test_recommend_without_model(self, client):
        """Teste: Recomendação sem modelo carregado"""
        response = client.post(
            '/api/v1/recommend',
            json={'query': 'Máquina vibrando muito'}
        )
        assert response.status_code == 503
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'não carregado' in data['error'].lower()
        print("✓ Validação modelo não carregado OK")
    
    def test_recommend_missing_query(self, client):
        """Teste: Query ausente"""
        response = client.post('/api/v1/recommend', json={})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'query' in data['error'].lower()
        print("✓ Validação query obrigatória OK")
    
    def test_recommend_empty_query(self, client):
        """Teste: Query vazia"""
        response = client.post(
            '/api/v1/recommend',
            json={'query': '   '}
        )
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        print("✓ Validação query vazia OK")
    
    def test_recommend_invalid_top_k_high(self, client):
        """Teste: top_k acima do limite"""
        response = client.post(
            '/api/v1/recommend',
            json={'query': 'Test', 'top_k': 100}
        )
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'top_k' in data['error'].lower()
        print("✓ Validação top_k máximo OK")
    
    def test_recommend_invalid_top_k_low(self, client):
        """Teste: top_k abaixo do mínimo"""
        response = client.post(
            '/api/v1/recommend',
            json={'query': 'Test', 'top_k': 0}
        )
        assert response.status_code == 400
        print("✓ Validação top_k mínimo OK")
    
    def test_recommend_invalid_min_score_high(self, client):
        """Teste: min_score acima de 1.0"""
        response = client.post(
            '/api/v1/recommend',
            json={'query': 'Test', 'min_score': 1.5}
        )
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'min_score' in data['error'].lower()
        print("✓ Validação min_score máximo OK")
    
    def test_recommend_invalid_min_score_low(self, client):
        """Teste: min_score negativo"""
        response = client.post(
            '/api/v1/recommend',
            json={'query': 'Test', 'min_score': -0.5}
        )
        assert response.status_code == 400
        print("✓ Validação min_score mínimo OK")
    
    @patch('api.engine')
    def test_recommend_success(self, mock_engine, client):
        """Teste: Recomendação bem-sucedida"""
        mock_engine.recommend.return_value = [
            {
                'product_id': 'TEST001',
                'product_name': 'Rolamento Teste',
                'score': 0.95,
                'bearing_type': 'Esférico',
                'price': 150.00,
                'technical_description': 'Teste'
            }
        ]
        
        response = client.post(
            '/api/v1/recommend',
            json={
                'query': 'Máquina vibrando muito',
                'top_k': 3,
                'min_score': 0.1
            }
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'query' in data
        assert 'num_results' in data
        assert 'recommendations' in data
        assert isinstance(data['recommendations'], list)
        
        # Verifica que o método foi chamado com parâmetros corretos
        mock_engine.recommend.assert_called_once_with(
            query='Máquina vibrando muito',
            top_k=3,
            min_score=0.1
        )
        print("✓ Recomendação bem-sucedida OK")


class TestAPIBatchRecommend:
    """Testes de recomendação em batch"""
    
    @patch('api.engine', None)
    def test_batch_without_model(self, client):
        """Teste: Batch sem modelo carregado"""
        response = client.post(
            '/api/v1/batch-recommend',
            json={'queries': ['Query 1', 'Query 2']}
        )
        assert response.status_code == 503
        
        data = json.loads(response.data)
        assert 'error' in data
        print("✓ Validação batch sem modelo OK")
    
    def test_batch_missing_queries(self, client):
        """Teste: Campo queries ausente"""
        response = client.post('/api/v1/batch-recommend', json={})
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert 'queries' in data['error'].lower()
        print("✓ Validação queries obrigatório OK")
    
    def test_batch_empty_list(self, client):
        """Teste: Lista vazia de queries"""
        response = client.post(
            '/api/v1/batch-recommend',
            json={'queries': []}
        )
        assert response.status_code == 400
        print("✓ Validação lista vazia OK")
    
    def test_batch_too_many_queries(self, client):
        """Teste: Mais de 50 queries"""
        queries = [f'Query {i}' for i in range(60)]
        response = client.post(
            '/api/v1/batch-recommend',
            json={'queries': queries}
        )
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
        assert '50' in data['error']
        print("✓ Validação limite batch OK")
    
    @patch('api.engine')
    def test_batch_success(self, mock_engine, client):
        """Teste: Batch bem-sucedido"""
        mock_engine.recommend.return_value = [
            {'product_id': 'TEST001', 'score': 0.9}
        ]
        
        response = client.post(
            '/api/v1/batch-recommend',
            json={
                'queries': ['Vibração', 'Superaquecimento'],
                'top_k': 2
            }
        )
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'num_queries' in data
        assert 'results' in data
        assert data['num_queries'] == 2
        assert isinstance(data['results'], dict)
        print("✓ Batch bem-sucedido OK")


class TestAPIErrorHandlers:
    """Testes de handlers de erro"""
    
    def test_404_not_found(self, client):
        """Teste: Endpoint não encontrado"""
        response = client.get('/api/v1/endpoint-invalido')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
        print("✓ 404 handler OK")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])