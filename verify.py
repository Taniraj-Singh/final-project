import requests
import time

def verify_fix():
    base_url = "http://localhost:8001"

    print("🔍 Verifying Model Loading Fix")
    print("=" * 50)

    # Check health
    health = requests.get(f"{base_url}/health").json()
    print(f"Models loaded: {health['models_loaded']}")
    print(f"Model status: {health['model_status']}")

    if health['models_loaded']:
        print("✅ SUCCESS: Models loaded correctly!")
        print("🎯 Now test predictions in Swagger UI: http://localhost:8001/docs")
    else:
        print("❌ FAILED: Models still not loading")
        print("💡 Check the model files in the models/ directory")

if __name__ == "__main__":
    verify_fix()