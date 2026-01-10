# test_recommendation_engine.py (executar uma vez)

import pandas as pd
from src.recommendation_engine import RecommendationEngine

# 1. Carregar dados
print("1. Carregando dados...")
products = pd.read_parquet('data/refined/products_features.parquet')
print(f"{len(products)} produtos carregados")

# 2. Instanciar e treinar
print("\n2. Treinando engine...")
engine = RecommendationEngine()
engine.fit(products)
print(f"Engine treinado")
print(f"Info: {engine.get_info()}")

# 3. Testar com 3 queries
print("\n3. Testando recomendações...")
test_queries = [
    "Minha máquina está vibrando muito",
    "Problema de superaquecimento",
    "Desgaste rápido do rolamento"
]

for query in test_queries:
    results = engine.recommend(query, top_k=3)
    print(f"\n   Query: '{query}'")
    for r in results:
        print(f"     → {r['product_name'][:30]}... (score: {r['score']:.3f})")

# 4. Salvar modelo
print("\n4. Salvando modelo...")
engine.save_model('models/recommendation_engine.pkl')
print(f"Modelo salvo em models/recommendation_engine.pkl")

# 5. Carregar e validar
print("\n5. Carregando e validando...")
loaded_engine = RecommendationEngine.load_model('models/recommendation_engine.pkl')
loaded_results = loaded_engine.recommend("Vibração", top_k=2)
print(f"Modelo carregado com sucesso")
print(f"   Teste: {len(loaded_results)} produtos recomendados")

print("\nTUDO OK! Classe está funcionando.")
