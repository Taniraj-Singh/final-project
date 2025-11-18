#!/usr/bin/env python3
"""
Frontend-Backend Integration Test
Tests all endpoints that the frontend will use
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def test_frontend_integration():
    print("🧪 Frontend-Backend Integration Test")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✅ Health check passed")
    
    # Test 2: Authentication
    print("\n2. Testing Authentication...")
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    print("✅ Authentication successful")
    
    # Test 3: Data Sources (Frontend: DataSources.jsx)
    print("\n3. Testing Data Sources...")
    response = requests.get(f"{BASE_URL}/datasources/", headers=headers)
    assert response.status_code == 200
    data_sources = response.json()
    print(f"✅ Found {len(data_sources)} data sources")
    
    # Test 4: Machines (Frontend: LineMachines.jsx)
    print("\n4. Testing Machines...")
    response = requests.get(f"{BASE_URL}/machines/", headers=headers)
    assert response.status_code == 200
    machines = response.json()
    print(f"✅ Found {len(machines)} machines")
    
    # Test 5: Alarms (Frontend: AlarmEvents.jsx)
    print("\n5. Testing Alarms...")
    response = requests.get(f"{BASE_URL}/alarms/", headers=headers)
    assert response.status_code == 200
    alarms = response.json()
    print(f"✅ Found {len(alarms)} alarms")
    
    # Test 6: Tickets (Frontend: MaintenancePlanner.jsx)
    print("\n6. Testing Tickets...")
    response = requests.get(f"{BASE_URL}/tickets/", headers=headers)
    assert response.status_code == 200
    tickets = response.json()
    print(f"✅ Found {len(tickets)} tickets")
    
    # Test 7: Reports (Frontend: Reports.jsx)
    print("\n7. Testing Reports...")
    if machines:
        machine_id = machines[0]["id"]
        start_time = (datetime.now() - timedelta(days=7)).isoformat()
        end_time = datetime.now().isoformat()
        
        # OEE Report
        response = requests.get(
            f"{BASE_URL}/reports/oee",
            params={
                "machine_id": machine_id,
                "start": start_time,
                "end": end_time
            },
            headers=headers
        )
        assert response.status_code == 200
        oee_data = response.json()
        print("✅ OEE report generated")
        
        # Availability Report
        response = requests.get(
            f"{BASE_URL}/reports/availability",
            params={
                "machine_id": machine_id,
                "start": start_time,
                "end": end_time
            },
            headers=headers
        )
        assert response.status_code == 200
        print("✅ Availability report generated")
    
    # Test 8: User Roles (Frontend: UserRoles.jsx)
    print("\n8. Testing User Roles...")
    response = requests.get(f"{BASE_URL}/user-roles/roles", headers=headers)
    assert response.status_code == 200
    roles = response.json()
    print(f"✅ Found {len(roles)} roles")
    
    response = requests.get(f"{BASE_URL}/user-roles/permissions", headers=headers)
    assert response.status_code == 200
    permissions = response.json()
    print(f"✅ Found {len(permissions)} permissions")
    
    # Test 9: Security Policies
    print("\n9. Testing Security Policies...")
    response = requests.get(f"{BASE_URL}/user-roles/security-policies", headers=headers)
    assert response.status_code == 200
    policies = response.json()
    print(f"✅ Found {len(policies)} security policies")
    
    # Test 10: IP Allowlist
    print("\n10. Testing IP Allowlist...")
    response = requests.get(f"{BASE_URL}/user-roles/ip-allowlist", headers=headers)
    assert response.status_code == 200
    allowlist = response.json()
    print(f"✅ Found {len(allowlist)} IP allowlist entries")
    
    print("\n" + "=" * 50)
    print("🎉 ALL FRONTEND-BACKEND INTEGRATION TESTS PASSED!")
    print("✅ Your frontend can now connect to the backend successfully!")
    print("\n📋 Integration Summary:")
    print(f"   • Data Sources: {len(data_sources)} configured")
    print(f"   • Machines: {len(machines)} available")
    print(f"   • Alarms: {len(alarms)} active")
    print(f"   • Tickets: {len(tickets)} created")
    print(f"   • Roles: {len(roles)} configured")
    print(f"   • Permissions: {len(permissions)} available")
    print(f"   • Security Policies: {len(policies)} active")
    
    print("\n🔗 Frontend Integration Ready!")
    print("   • API Base URL: http://127.0.0.1:8000")
    print("   • API Docs: http://127.0.0.1:8000/docs")
    print("   • Admin Login: admin@example.com / admin123")

if __name__ == "__main__":
    try:
        test_frontend_integration()
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        exit(1)
