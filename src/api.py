from flask import Flask, request, jsonify
from recommendation_engine import RecommendationEngine
import json
from pathlib import Path
import logging
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)

# Definir caminhos relativos (a partir da raiz do projeto)
BASE_DIR = Path(__file__).parent.parent  # Sobe para a raiz do projeto
MODEL_PATH = BASE_DIR / 'models' / 'recommendation_engine.pkl'
METADATA_PATH = BASE_DIR / 'models' / 'model_metadata.json'

print(f"DEBUG: BASE_DIR = {BASE_DIR}")
print(f"DEBUG: MODEL_PATH = {MODEL_PATH}")
print(f"DEBUG: MODEL_PATH existe? {MODEL_PATH.exists()}")
print(f"DEBUG: METADATA_PATH = {METADATA_PATH}")
print(f"DEBUG: METADATA_PATH existe? {METADATA_PATH.exists()}")

# Carregar modelo na memória
engine = None
metadata = {}

try:
    if MODEL_PATH.exists():
        engine = RecommendationEngine.load_model(str(MODEL_PATH))
        logger.info(f"Modelo carregado: {MODEL_PATH}")
    else:
        logger.error(f"Arquivo não encontrado: {MODEL_PATH}")
except Exception as e:
    logger.error(f"Erro ao carregar modelo: {e}")
    import traceback
    traceback.print_exc()

# Carregar metadata
try:
    if METADATA_PATH.exists():
        with open(METADATA_PATH, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        logger.info(f"Metadata carregado: {METADATA_PATH}")
    else:
        logger.error(f"Arquivo não encontrado: {METADATA_PATH}")
except Exception as e:
    logger.error(f"Erro ao carregar metadata: {e}")
    import traceback
    traceback.print_exc()


# ============================================================================
# ROTAS
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': engine is not None,
        'timestamp': str(pd.Timestamp.now())
    }), 200


@app.route('/api/v1/metadata', methods=['GET'])
def get_metadata():
    """Retornar metadata do modelo"""
    if not metadata:
        return jsonify({
            'error': 'Metadata não disponível'
        }), 503
    return jsonify(metadata), 200


@app.route('/api/v1/recommend', methods=['POST'])
def recommend():
    """
    Endpoint de recomendação
    
    Body JSON:
    {
        "query": "Máquina vibrando muito",
        "top_k": 5,
        "min_score": 0.1
    }
    """
    if engine is None:
        return jsonify({
            'error': 'Modelo não carregado'
        }), 503
    
    try:
        data = request.get_json()
        
        # Validar input
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Campo "query" é obrigatório'
            }), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({
                'error': 'Query não pode estar vazia'
            }), 400
        
        top_k = int(data.get('top_k', 5))
        min_score = float(data.get('min_score', 0.0))
        
        # Validar ranges
        if top_k < 1 or top_k > 20:
            return jsonify({
                'error': 'top_k deve estar entre 1 e 20'
            }), 400
        
        if min_score < 0.0 or min_score > 1.0:
            return jsonify({
                'error': 'min_score deve estar entre 0.0 e 1.0'
            }), 400
        
        # Gerar recomendações
        recommendations = engine.recommend(
            query=query,
            top_k=top_k,
            min_score=min_score
        )
        
        return jsonify({
            'query': query,
            'num_results': len(recommendations),
            'recommendations': recommendations
        }), 200
    
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        return jsonify({
            'error': f'Erro de validação: {str(e)}'
        }), 400
    except Exception as e:
        logger.error(f"Erro ao processar recomendação: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Erro ao processar: {str(e)}'
        }), 500


@app.route('/api/v1/batch-recommend', methods=['POST'])
def batch_recommend():
    """
    Endpoint de recomendação em batch
    
    Body JSON:
    {
        "queries": ["Query 1", "Query 2", "Query 3"],
        "top_k": 3
    }
    """
    if engine is None:
        return jsonify({
            'error': 'Modelo não carregado'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'queries' not in data:
            return jsonify({
                'error': 'Campo "queries" é obrigatório'
            }), 400
        
        queries = data['queries']
        if not isinstance(queries, list) or len(queries) == 0:
            return jsonify({
                'error': 'queries deve ser uma lista não-vazia'
            }), 400
        
        if len(queries) > 50:
            return jsonify({
                'error': 'Máximo de 50 queries por batch'
            }), 400
        
        top_k = int(data.get('top_k', 5))
        min_score = float(data.get('min_score', 0.0))
        
        # Validar ranges
        if top_k < 1 or top_k > 20:
            return jsonify({
                'error': 'top_k deve estar entre 1 e 20'
            }), 400
        
        # Processar batch
        results = {}
        for query in queries:
            if query.strip():
                results[query] = engine.recommend(
                    query=query,
                    top_k=top_k,
                    min_score=min_score
                )
        
        return jsonify({
            'num_queries': len(queries),
            'results': results
        }), 200
    
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        return jsonify({
            'error': f'Erro de validação: {str(e)}'
        }), 400
    except Exception as e:
        logger.error(f"Erro ao processar batch: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Erro ao processar: {str(e)}'
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"Erro 500: {error}")
    return jsonify({'error': 'Erro interno do servidor'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════╗
║         API DE RECOMENDAÇÃO DE ROLAMENTOS - SERVIDOR         ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    print("Endpoints disponíveis:")
    print("• GET  /health                    - Health check")
    print("• GET  /api/v1/metadata           - Metadata do modelo")
    print("• POST /api/v1/recommend          - Recomendação única")
    print("• POST /api/v1/batch-recommend    - Recomendação em batch")
    print("\nIniciando servidor...")
    print("   Acesse: http://localhost:5000\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)