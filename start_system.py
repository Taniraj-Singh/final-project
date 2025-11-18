import subprocess
import sys
import time
import os
from main import app
import uvicorn
import threading

def start_mosquitto():
    """Start Mosquitto MQTT broker automatically"""
    try:
        print("🚀 Starting Mosquitto MQTT Broker...")
        
        # Try different ways to start Mosquitto
        try:
            # Windows with chocolatey
            subprocess.Popen(["mosquitto", "-v"], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
        except:
            try:
                # Linux/Mac
                subprocess.Popen(["mosquitto", "-v"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
            except:
                # Docker fallback
                print("📦 Starting Mosquitto via Docker...")
                subprocess.Popen(["docker", "run", "-p", "1883:1883", "-p", "9001:9001", 
                                "eclipse-mosquitto"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        
        print("⏳ Waiting for MQTT broker to start...")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Could not start MQTT broker: {e}")
        return False

def start_fastapi():
    """Start FastAPI server"""
    print("🌐 Starting FastAPI Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    # Try to start MQTT broker
    mqtt_started = start_mosquitto()
    
    if mqtt_started:
        print("✅ MQTT Broker started successfully!")
    else:
        print("⚠️  Using simulated data mode (MQTT not available)")
    
    # Start FastAPI
    start_fastapi()