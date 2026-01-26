"""
Script de teste do sistema de monitoramento
"""
import sys
import os
import streamlit as st

sys.path.insert(0, os.path.abspath('../src'))

print("Testando Sistema de Monitoramento\n")


# Teste 1: Import
print("1️⃣ Testando imports...")
try:
    from data_app.monitoring import StreamlitMonitor, CONFIG
    print("StreamlitMonitor importado")
    print("CONFIG importado")
except ImportError as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)

# Teste 2: Inicialização
print("\n2️⃣ Testando inicialização...")
try:
    monitor = StreamlitMonitor()
    print("Monitor inicializado")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 3: Baseline
print("\n3️⃣ Testando baseline...")
try:
    import numpy as np
    baseline_array = np.random.beta(8, 2, 300)
    baseline = baseline_array.tolist()  # Converter para lista
    status = monitor.initialize_baseline(baseline)
    print(f"Baseline configurado: {status['samples']} amostras")
    print(f"Média: {status['mean']:.3f}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 4: Track Recommendation
print("\n4️⃣ Testando rastreamento de predição...")
try:
    recommendations = [
        {'product_id': 'P001', 'score': 0.85},
        {'product_id': 'P002', 'score': 0.78}
    ]
    
    result = monitor.track_recommendation(
        query="Rolamento teste",
        recommendations=recommendations,
        processing_time=0.15
    )
    
    print(f"Predição rastreada")
    print(f"Processing time: {result['processing_time_ms']:.1f}ms")
    print(f"Top score: {result['top_score']:.1%}")
    print(f"Drift detected: {result['drift_detected']}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 5: System Health
print("\n5️⃣ Testando monitoramento de sistema...")
try:
    health = monitor.track_system_health()
    print(f"Status: {health['status']}")
    print(f"CPU: {health['cpu_usage']:.1f}%")
    print(f"Memory: {health['memory_usage']:.1f}%")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 6: Dashboard
print("\n6️⃣ Testando dashboard...")
try:
    dashboard = monitor.get_dashboard_metrics(hours=24)
    print(f"Dashboard gerado")
    print(f"Total queries: {dashboard['summary']['total_predictions']}")
    print(f"Drift detected: {dashboard['drift']['detected']}")
    print(f"Alertas ativos: {dashboard['alerts']['active']}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Teste 7: Alertas
print("\n7️⃣ Testando sistema de alertas...")
try:
    # Simular CPU alta
    monitor.alerts.check_cpu_usage(85)
    active = monitor.alerts.get_active_alerts()
    print(f"Alertas funcionando: {len(active)} alertas")
    
    if active:
        print(f"Primeiro alerta: {active[0]['title']}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("TODOS OS TESTES PASSARAM!")
print("="*50)
print("\nSistema de monitoramento está funcionando corretamente!")
