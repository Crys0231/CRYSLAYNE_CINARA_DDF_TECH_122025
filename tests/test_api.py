import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.abspath('../src'))

import pytest
import json
from api import app


@pytest.fixture
def client():
    """Cliente Flask para testes"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAPI:
    """Suite de testes para a API"""
    
    def test_health(self, client):
        """Teste: Health check"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        print(f"Health check OK")
    
    def test_metadata_unavailable(self, client):
        """Teste: Metadata não disponível (esperado em testes)"""
        response = client.get('/api/v1/metadata')
        # Em teste, o modelo não está carregado, então esperamos 503
        assert response.status_code in [200, 503]
        print(f"Metadata teste OK (status: {response.status_code})")
    
    def test_recommend_model_unavailable(self, client):
        """Teste: Recomendação sem modelo (esperado em testes)"""
        response = client.post(
            '/api/v1/recommend',
            json={
                'query': 'Máquina vibrando muito',
                'top_k': 3
            }
        )
        # Em teste, o modelo não está carregado, então esperamos 503
        assert response.status_code == 503
        data = json.loads(response.data)
        assert 'error' in data
        print(f"Validação OK: Modelo não disponível")
    
    def test_recommend_missing_query(self, client):
        """Teste: Query ausente"""
        response = client.post(
            '/api/v1/recommend',
            json={}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        print(f"Validação OK: Query obrigatória")
    
    def test_recommend_invalid_top_k(self, client):
        """Teste: top_k fora do range"""
        response = client.post(
            '/api/v1/recommend',
            json={
                'query': 'Test',
                'top_k': 100  # > 20
            }
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        print(f"Validação OK: top_k range")
    
    def test_recommend_model_unavailable(self, client):
        """Teste: Recomendação com modelo (esperado em testes com modelo)"""
        response = client.post(
            '/api/v1/recommend',
            json={
                'query': 'Máquina vibrando muito',
                'top_k': 3
            }
        )
        # Modelo está carregado, então esperamos 200 OK
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'recommendations' in data or 'num_results' in data
        print(f"Recomendação OK: Modelo disponível")
    
    def test_batch_recommend_model_unavailable(self, client):
        """Teste: Batch com modelo (esperado em testes com modelo)"""
        response = client.post(
            '/api/v1/batch-recommend',
            json={
                'queries': [
                    'Vibração',
                    'Superaquecimento'
                ],
                'top_k': 2
            }
        )
        # Modelo está carregado, então esperamos 200 OK
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data or 'num_queries' in data
        print(f"Batch OK: Modelo disponível")

    
    def test_batch_recommend_missing_queries(self, client):
        """Teste: Batch sem queries"""
        response = client.post(
            '/api/v1/batch-recommend',
            json={}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        print(f"Validação OK: queries obrigatório")
    
    def test_batch_recommend_too_many(self, client):
        """Teste: Batch com >50 queries"""
        queries = [f'Query {i}' for i in range(60)]
        response = client.post(
            '/api/v1/batch-recommend',
            json={'queries': queries}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        print(f"Validação OK: Batch max 50")
    
    def test_not_found(self, client):
        """Teste: Endpoint não encontrado"""
        response = client.get('/api/v1/nao-existe')
        assert response.status_code == 404
        print(f"404 OK: Endpoint não encontrado")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
