# start_service.py
import subprocess
import time
import requests
import sys
import os

def check_service_running():
    """Check if the service is already running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_service():
    print("🚀 Starting Nozzle Degradation Service...")
    
    # Check if service is already running
    if check_service_running():
        print("✅ Service is already running!")
        print("📖 Open: http://localhost:8000/docs")
        return
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found!")
        print("📁 Current directory files:")
        for file in os.listdir("."):
            print(f"  - {file}")
        return
    
    # Start the FastAPI service
    try:
        print("🔧 Starting uvicorn server...")
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
        
        print("⏳ Waiting for service to start (10 seconds)...")
        time.sleep(10)  # Wait longer for service to start
        
        # Test the service
        print("🔍 Testing service health...")
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Service started successfully!")
                print(f"📊 Status: {data.get('status', 'unknown')}")
                print(f"🔧 Models loaded: {data.get('models_loaded', 'unknown')}")
                print("📖 Open API documentation at: http://localhost:8000/docs")
                print("\n🎯 Ready for testing! Press Ctrl+C to stop the service.")
                
                # Keep the service running
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Service stopped by user")
                    process.terminate()
            else:
                print(f"❌ Service returned status code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to service: {e}")
            print("💡 Try running manually: uvicorn main:app --reload")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        print("💡 Make sure you have installed dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    start_service()