#!/usr/bin/env python3
"""
Comprehensive Frontend-Backend Integration Test
Tests all Phase 2 functionality and data flow
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:5173"

class IntegrationTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.test_results = []

    def log_test(self, test_name, success, message=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def authenticate(self):
        """Test authentication flow"""
        try:
            # Test login
            login_data = {
                "username": "admin@example.com",
                "password": "admin123"
            }
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.access_token}"
                })
                self.log_test("Authentication", True, "Successfully logged in")
                return True
            else:
                self.log_test("Authentication", False, f"Login failed: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Authentication", False, f"Login error: {str(e)}")
            return False

    def test_machines_api(self):
        """Test machines API endpoints"""
        try:
            # Test GET machines
            response = self.session.get(f"{BASE_URL}/machines/")
            if response.status_code == 200:
                machines = response.json()
                self.log_test("Machines API - GET", True, f"Retrieved {len(machines)} machines")
                
                # Test creating a machine
                new_machine = {
                    "name": f"Test Machine {datetime.now().strftime('%H%M%S')}",
                    "line": "Test Line",
                    "location": "Test Location",
                    "status": "running",
                    "oee_percentage": 85.5,
                    "anomaly_score": 0.2,
                    "machine_type": "CNC",
                    "manufacturer": "Test Manufacturer",
                    "model": "TM-1000",
                    "serial_number": f"SN{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "is_active": True
                }
                
                create_response = self.session.post(f"{BASE_URL}/machines/", json=new_machine)
                if create_response.status_code == 200:
                    created_machine = create_response.json()
                    self.log_test("Machines API - CREATE", True, f"Created machine: {created_machine['name']}")
                    
                    # Test updating machine
                    update_data = {"status": "maintenance", "oee_percentage": 90.0}
                    update_response = self.session.put(f"{BASE_URL}/machines/{created_machine['id']}", json=update_data)
                    if update_response.status_code == 200:
                        self.log_test("Machines API - UPDATE", True, "Successfully updated machine")
                    else:
                        self.log_test("Machines API - UPDATE", False, f"Update failed: {update_response.status_code}")
                    
                    return created_machine
                else:
                    self.log_test("Machines API - CREATE", False, f"Create failed: {create_response.status_code}")
            else:
                self.log_test("Machines API - GET", False, f"GET failed: {response.status_code}")
        except Exception as e:
            self.log_test("Machines API", False, f"Error: {str(e)}")
        return None

    def test_alarms_api(self):
        """Test alarms API endpoints"""
        try:
            # Test GET alarms
            response = self.session.get(f"{BASE_URL}/alarms/")
            if response.status_code == 200:
                alarms = response.json()
                self.log_test("Alarms API - GET", True, f"Retrieved {len(alarms)} alarms")
                
                # Get a valid machine ID first
                machines_response = self.session.get(f"{BASE_URL}/machines/")
                if machines_response.status_code == 200 and machines_response.json():
                    machine_id = machines_response.json()[0]["id"]
                    
                    # Test creating an alarm
                    new_alarm = {
                        "machine_id": machine_id,
                        "sensor_type": "temperature",
                        "severity": "Hoch",
                        "message": "Temperature threshold exceeded",
                        "equipment_name": "Test Equipment",
                        "source": "sensor",
                        "threshold_value": 80.0,
                        "actual_value": 85.5,
                        "category": "temperature",
                        "priority": 2
                    }
                
                    create_response = self.session.post(f"{BASE_URL}/alarms/", json=new_alarm)
                    if create_response.status_code == 200:
                        created_alarm = create_response.json()
                        self.log_test("Alarms API - CREATE", True, f"Created alarm: {created_alarm['message']}")
                        
                        # Test acknowledging alarm
                        ack_response = self.session.post(
                            f"{BASE_URL}/alarms/{created_alarm['id']}/acknowledge",
                            json={"acknowledged_by": "test_user"}
                        )
                        if ack_response.status_code == 200:
                            self.log_test("Alarms API - ACKNOWLEDGE", True, "Successfully acknowledged alarm")
                        else:
                            self.log_test("Alarms API - ACKNOWLEDGE", False, f"Acknowledge failed: {ack_response.status_code}")
                        
                        return created_alarm
                    else:
                        self.log_test("Alarms API - CREATE", False, f"Create failed: {create_response.status_code}")
                else:
                    self.log_test("Alarms API - CREATE", False, "No machines available for alarm creation")
            else:
                self.log_test("Alarms API - GET", False, f"GET failed: {response.status_code}")
        except Exception as e:
            self.log_test("Alarms API", False, f"Error: {str(e)}")
        return None

    def test_tickets_api(self):
        """Test tickets API endpoints"""
        try:
            # Test GET tickets
            response = self.session.get(f"{BASE_URL}/tickets/")
            if response.status_code == 200:
                tickets = response.json()
                self.log_test("Tickets API - GET", True, f"Retrieved {len(tickets)} tickets")
                
                # Get a valid machine ID first
                machines_response = self.session.get(f"{BASE_URL}/machines/")
                if machines_response.status_code == 200 and machines_response.json():
                    machine_id = machines_response.json()[0]["id"]
                    
                    # Test creating a ticket
                    new_ticket = {
                        "title": f"Test Maintenance Ticket {datetime.now().strftime('%H%M%S')}",
                        "description": "Test ticket created via API",
                        "status": "open",
                        "priority": "Medium",
                        "ticket_type": "maintenance",
                        "category": "preventive",
                        "machine_id": machine_id
                    }
                
                    create_response = self.session.post(f"{BASE_URL}/tickets/", json=new_ticket)
                    if create_response.status_code == 200:
                        created_ticket = create_response.json()
                        self.log_test("Tickets API - CREATE", True, f"Created ticket: {created_ticket['title']}")
                        
                        # Test updating ticket status
                        update_response = self.session.put(
                            f"{BASE_URL}/tickets/{created_ticket['id']}",
                            json={"status": "in_progress"}
                        )
                        if update_response.status_code == 200:
                            self.log_test("Tickets API - UPDATE", True, "Successfully updated ticket status")
                        else:
                            self.log_test("Tickets API - UPDATE", False, f"Update failed: {update_response.status_code}")
                        
                        return created_ticket
                    else:
                        self.log_test("Tickets API - CREATE", False, f"Create failed: {create_response.status_code}")
                else:
                    self.log_test("Tickets API - CREATE", False, "No machines available for ticket creation")
            else:
                self.log_test("Tickets API - GET", False, f"GET failed: {response.status_code}")
        except Exception as e:
            self.log_test("Tickets API", False, f"Error: {str(e)}")
        return None

    def test_datasources_api(self):
        """Test data sources API endpoints"""
        try:
            # Test GET data sources
            response = self.session.get(f"{BASE_URL}/datasources/")
            if response.status_code == 200:
                datasources = response.json()
                self.log_test("DataSources API - GET", True, f"Retrieved {len(datasources)} data sources")
                
                # Test creating a data source
                new_datasource = {
                    "name": f"Test MQTT Source {datetime.now().strftime('%H%M%S')}",
                    "protocol": "MQTT",
                    "connection_config": {
                        "broker_url": "mqtt://test-broker:1883",
                        "topic": "sensors/+/data",
                        "client_id": "test_client"
                    },
                    "sampling_interval_ms": 1000,
                    "units_policy": "from_payload",
                    "gap_handling_strategy": "interpolate",
                    "is_active": True
                }
                
                create_response = self.session.post(f"{BASE_URL}/datasources/", json=new_datasource)
                if create_response.status_code == 200:
                    created_datasource = create_response.json()
                    self.log_test("DataSources API - CREATE", True, f"Created data source: {created_datasource['name']}")
                    return created_datasource
                else:
                    self.log_test("DataSources API - CREATE", False, f"Create failed: {create_response.status_code}")
            else:
                self.log_test("DataSources API - GET", False, f"GET failed: {response.status_code}")
        except Exception as e:
            self.log_test("DataSources API", False, f"Error: {str(e)}")
        return None

    def test_reports_api(self):
        """Test reports API endpoints"""
        try:
            # Get a valid machine ID first
            machines_response = self.session.get(f"{BASE_URL}/machines/")
            if machines_response.status_code == 200 and machines_response.json():
                machine_id = machines_response.json()[0]["id"]
                
                # Test generating a report
                report_params = {
                    "type": "oee",
                    "format": "csv",
                    "start_date": (datetime.now() - timedelta(days=7)).isoformat(),
                    "end_date": datetime.now().isoformat(),
                    "machine_id": machine_id
                }
                
                response = self.session.get(f"{BASE_URL}/reports/generate", params=report_params)
                if response.status_code == 200:
                    self.log_test("Reports API - GENERATE", True, "Successfully generated report")
                else:
                    self.log_test("Reports API - GENERATE", False, f"Generate failed: {response.status_code}")
            else:
                self.log_test("Reports API - GENERATE", False, "No machines available for report generation")
        except Exception as e:
            self.log_test("Reports API", False, f"Error: {str(e)}")

    def test_user_roles_api(self):
        """Test user roles API endpoints"""
        try:
            # Test GET roles
            response = self.session.get(f"{BASE_URL}/user-roles/roles")
            if response.status_code == 200:
                roles = response.json()
                self.log_test("User Roles API - GET ROLES", True, f"Retrieved {len(roles)} roles")
            else:
                self.log_test("User Roles API - GET ROLES", False, f"GET roles failed: {response.status_code}")
            
            # Test GET users
            response = self.session.get(f"{BASE_URL}/auth/users")
            if response.status_code == 200:
                users = response.json()
                self.log_test("User Roles API - GET USERS", True, f"Retrieved {len(users)} users")
            else:
                self.log_test("User Roles API - GET USERS", False, f"GET users failed: {response.status_code}")
        except Exception as e:
            self.log_test("User Roles API", False, f"Error: {str(e)}")

    def test_frontend_connectivity(self):
        """Test frontend connectivity"""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Connectivity", True, "Frontend is accessible")
            else:
                self.log_test("Frontend Connectivity", False, f"Frontend returned status: {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Connectivity", False, f"Frontend not accessible: {str(e)}")

    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 Starting Frontend-Backend Integration Tests")
        print("=" * 60)
        
        # Test authentication first
        if not self.authenticate():
            print("❌ Authentication failed. Cannot proceed with other tests.")
            return
        
        # Run all API tests
        self.test_machines_api()
        self.test_alarms_api()
        self.test_tickets_api()
        self.test_datasources_api()
        self.test_reports_api()
        self.test_user_roles_api()
        self.test_frontend_connectivity()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Save detailed results
        with open("integration_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: integration_test_results.json")
        
        if passed == total:
            print("\n🎉 All tests passed! Frontend-Backend integration is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} tests failed. Please check the logs above.")

if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_all_tests()
