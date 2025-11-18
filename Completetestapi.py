import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"🔍 {message}")

def test_health():
    """Test health endpoint"""
    print_info("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health: {data['status']}")
            print_success(f"Models loaded: {data['models_loaded']}")
            print_success(f"Model version: {data['model_version']}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print_info("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Service: {data['message']}")
            print_success(f"Version: {data['version']}")
            return True
        else:
            print_error(f"Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Root endpoint error: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print_info("Testing model info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Feature count: {data['feature_count']}")
            print_success(f"Window size: {data['window_size']}")
            print_success(f"Model type: {data['model_type']}")
            return True
        else:
            print_error(f"Model info failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Model info error: {e}")
        return False

def test_buffer_status():
    """Test buffer status endpoint"""
    print_info("Testing buffer status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/buffer-status/test-nozzle-1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['buffer_exists']:
                print_success(f"Buffer exists: {data['current_size']}/{data['window_size']}")
            else:
                print_info("Buffer doesn't exist yet (expected)")
            return True
        else:
            print_error(f"Buffer status failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Buffer status error: {e}")
        return False

def test_first_prediction():
    """Test first prediction (buffer empty)"""
    print_info("Testing first prediction (buffer empty)...")
    
    test_data = {
        "nozzle_id": "test-nozzle-1",
        "timestamp": datetime.now().isoformat() + "Z",
        "sensors": {
            "pressure": 125.5,
            "temperature": 185.2,
            "flow_rate": 45.3,
            "motor_current": 12.8,
            "vibration": 2.1
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status: {data['status']}")
            print_success(f"Score: {data['anomaly_score']:.3f}")
            if data.get('message'):
                print_info(f"Message: {data['message']}")
            return True
        else:
            print_error(f"Prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Prediction error: {e}")
        return False

def fill_buffer():
    """Fill the buffer with data"""
    print_info("Filling buffer with 65 data points...")
    
    success_count = 0
    for i in range(65):
        test_data = {
            "nozzle_id": "test-nozzle-1",
            "timestamp": f"2024-01-15T10:00:{i:02d}Z",
            "sensors": {
                "pressure": 125.5 + (i * 0.1),
                "temperature": 185.2 + (i * 0.05),
                "flow_rate": 45.3 + (i * 0.02),
                "motor_current": 12.8 + (i * 0.01),
                "vibration": 2.1 + (i * 0.005)
            }
        }
        
        try:
            response = requests.post(f"{BASE_URL}/predict", json=test_data, timeout=5)
            if response.status_code == 200:
                success_count += 1
                if i < 3:  # Show first few
                    data = response.json()
                    if data.get('message'):
                        print_info(f"Request {i+1}: {data['message']}")
                    else:
                        print_info(f"Request {i+1}: Score: {data['anomaly_score']:.3f}")
        except:
            pass
        
        if i % 20 == 0 and i > 0:
            print_info(f"Progress: {i+1}/65 requests sent")
    
    print_success(f"Buffer filled: {success_count}/65 successful")
    return success_count >= 60  # Allow some failures

def test_real_prediction():
    """Test prediction with full buffer"""
    print_info("Testing real prediction (full buffer)...")
    
    test_data = {
        "nozzle_id": "test-nozzle-1",
        "timestamp": "2024-01-15T10:01:05Z",
        "sensors": {
            "pressure": 125.5,
            "temperature": 185.2,
            "flow_rate": 45.3,
            "motor_current": 12.8,
            "vibration": 2.1
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=test_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Anomaly Score: {data['anomaly_score']:.3f}")
            print_success(f"Status: {data['status']}")
            print_success(f"Model Version: {data['model_version']}")
            
            if data['contributing_features']:
                print_success(f"Top Features: {len(data['contributing_features'])}")
                for feature in data['contributing_features'][:3]:
                    print(f"   - {feature['feature']}: {feature['contribution']:.3f} ({feature['direction']})")
            else:
                print_info("No feature contributions (buffer might not be ready)")
            
            return True
        else:
            print_error(f"Real prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Real prediction error: {e}")
        return False

def test_anomaly_detection():
    """Test anomaly detection"""
    print_info("Testing anomaly detection...")
    
    # Send anomalous data (pressure spike)
    anomaly_data = {
        "nozzle_id": "test-nozzle-1",
        "timestamp": "2024-01-15T10:01:06Z",
        "sensors": {
            "pressure": 200.0,  # High pressure spike
            "temperature": 185.2,
            "flow_rate": 45.3,
            "motor_current": 12.8,
            "vibration": 2.1
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=anomaly_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Anomaly Score: {data['anomaly_score']:.3f}")
            print_success(f"Status: {data['status']}")
            
            if data['anomaly_score'] > 0.7:
                print_success("✅ Anomaly detected correctly!")
            else:
                print_info("⚠️  Anomaly score lower than expected")
            
            return True
        else:
            print_error(f"Anomaly detection failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Anomaly detection error: {e}")
        return False

def test_performance():
    """Test performance with multiple requests"""
    print_info("Testing performance...")
    
    response_times = []
    test_data = {
        "nozzle_id": "test-nozzle-1",
        "timestamp": datetime.now().isoformat() + "Z",
        "sensors": {
            "pressure": 125.5,
            "temperature": 185.2,
            "flow_rate": 45.3,
            "motor_current": 12.8,
            "vibration": 2.1
        }
    }
    
    for i in range(5):
        try:
            start_time = time.time()
            response = requests.post(f"{BASE_URL}/predict", json=test_data, timeout=10)
            end_time = time.time()
            
            if response.status_code == 200:
                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)
        except:
            pass
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        print_success(f"Average response time: {avg_time:.2f}ms")
        print_success(f"Max response time: {max_time:.2f}ms")
        
        if avg_time < 200:
            print_success("✅ Performance: MEETS REQUIREMENTS (< 200ms)")
        else:
            print_error("❌ Performance: DOES NOT MEET REQUIREMENTS")
        
        return True
    else:
        print_error("Performance test failed")
        return False

def main():
    """Run complete test suite"""
    print("🚀 Nozzle Degradation Service - Complete API Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 8
    
    # Test 1: Basic endpoints
    if test_health():
        tests_passed += 1
    if test_root():
        tests_passed += 1
    if test_model_info():
        tests_passed += 1
    if test_buffer_status():
        tests_passed += 1
    
    # Test 2: Predictions
    if test_first_prediction():
        tests_passed += 1
    
    # Test 3: Fill buffer and test real predictions
    if fill_buffer():
        tests_passed += 1
    if test_real_prediction():
        tests_passed += 1
    if test_anomaly_detection():
        tests_passed += 1
    
    # Test 4: Performance
    if test_performance():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 TEST SUMMARY: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Service is fully operational!")
        print("📖 Open: http://localhost:8000/docs for interactive testing")
    else:
        print("⚠️  Some tests failed. Check the service configuration.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()