#!/usr/bin/env python3
"""
Test script for Phase 2 API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_auth():
    """Test authentication"""
    print("\nTesting authentication...")
    
    # Test login
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"Login successful: {response.status_code}")
        return token
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_data_sources(token):
    """Test data sources endpoints"""
    print("\nTesting data sources endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test list data sources
    response = requests.get(f"{BASE_URL}/datasources", headers=headers)
    print(f"List data sources: {response.status_code}")
    if response.status_code == 200:
        datasources = response.json()
        print(f"Found {len(datasources)} data sources")
        
        if datasources:
            # Test get specific data source
            ds_id = datasources[0]["id"]
            response = requests.get(f"{BASE_URL}/datasources/{ds_id}", headers=headers)
            print(f"Get data source: {response.status_code}")
            
            # Test data source status
            response = requests.get(f"{BASE_URL}/datasources/{ds_id}/status", headers=headers)
            print(f"Data source status: {response.status_code}")
    
    # Test data source statistics
    response = requests.get(f"{BASE_URL}/datasources/statistics/summary", headers=headers)
    print(f"Data source statistics: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"Statistics: {stats}")

def test_machines(token):
    """Test machines endpoints"""
    print("\nTesting machines endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test list machines
    response = requests.get(f"{BASE_URL}/machines", headers=headers)
    print(f"List machines: {response.status_code}")
    if response.status_code == 200:
        machines = response.json()
        print(f"Found {len(machines)} machines")
        
        if machines:
            # Test get specific machine
            machine_id = machines[0]["id"]
            response = requests.get(f"{BASE_URL}/machines/{machine_id}", headers=headers)
            print(f"Get machine: {response.status_code}")

def test_alarms(token):
    """Test alarms endpoints"""
    print("\nTesting alarms endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test list alarms
    response = requests.get(f"{BASE_URL}/alarms", headers=headers)
    print(f"List alarms: {response.status_code}")
    if response.status_code == 200:
        alarms = response.json()
        print(f"Found {len(alarms)} alarms")
    
    # Test active alarms
    response = requests.get(f"{BASE_URL}/alarms/active", headers=headers)
    print(f"Active alarms: {response.status_code}")
    
    # Test alarm statistics
    response = requests.get(f"{BASE_URL}/alarms/statistics", headers=headers)
    print(f"Alarm statistics: {response.status_code}")

def test_tickets(token):
    """Test tickets endpoints"""
    print("\nTesting tickets endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test list tickets
    response = requests.get(f"{BASE_URL}/tickets", headers=headers)
    print(f"List tickets: {response.status_code}")
    if response.status_code == 200:
        tickets = response.json()
        print(f"Found {len(tickets)} tickets")
    
    # Test ticket statistics
    response = requests.get(f"{BASE_URL}/tickets/statistics/summary", headers=headers)
    print(f"Ticket statistics: {response.status_code}")

def test_reports(token):
    """Test reports endpoints"""
    print("\nTesting reports endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get a machine ID for reports
    response = requests.get(f"{BASE_URL}/machines", headers=headers)
    if response.status_code == 200 and response.json():
        machine_id = response.json()[0]["id"]
        
        # Test OEE report
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        params = {
            "machine_id": machine_id,
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        }
        
        response = requests.get(f"{BASE_URL}/reports/oee", headers=headers, params=params)
        print(f"OEE report: {response.status_code}")
        
        # Test availability report
        response = requests.get(f"{BASE_URL}/reports/availability", headers=headers, params=params)
        print(f"Availability report: {response.status_code}")

def test_user_roles(token):
    """Test user roles endpoints"""
    print("\nTesting user roles endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test list roles
    response = requests.get(f"{BASE_URL}/user-roles/roles", headers=headers)
    print(f"List roles: {response.status_code}")
    if response.status_code == 200:
        roles = response.json()
        print(f"Found {len(roles)} roles")
    
    # Test list permissions
    response = requests.get(f"{BASE_URL}/user-roles/permissions", headers=headers)
    print(f"List permissions: {response.status_code}")
    if response.status_code == 200:
        permissions = response.json()
        print(f"Found {len(permissions)} permissions")
    
    # Test security policies
    response = requests.get(f"{BASE_URL}/user-roles/security-policies", headers=headers)
    print(f"Security policies: {response.status_code}")
    
    # Test IP allowlist
    response = requests.get(f"{BASE_URL}/user-roles/ip-allowlist", headers=headers)
    print(f"IP allowlist: {response.status_code}")

def main():
    """Main test function"""
    print("Phase 2 API Testing")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("Health check failed. Is the server running?")
        return
    
    # Test authentication
    token = test_auth()
    if not token:
        print("Authentication failed. Please check credentials.")
        return
    
    # Test all endpoints
    test_data_sources(token)
    test_machines(token)
    test_alarms(token)
    test_tickets(token)
    test_reports(token)
    test_user_roles(token)
    
    print("\n" + "=" * 50)
    print("Phase 2 API testing completed!")

if __name__ == "__main__":
    main()
