# test_step1.py
from src.model_loader import load_system
print("Attempting to load system...")
try:
    model, data, cfg = load_system()
    print("✅ SUCCESS! Model loaded.")
    print(f"   - User Nodes: {data['user'].num_nodes}")
    print(f"   - App Name: {cfg['app_name']}")
except Exception as e:
    print(f"❌ FAILED: {e}")