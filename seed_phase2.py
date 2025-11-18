#!/usr/bin/env python3
"""
Seed script for Phase 2 - Populate database with initial roles, permissions, and data sources
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user_role import Role, Permission, RolePermission, SecurityPolicy, IPAllowlist
from app.models.datasource import DataSource
from app.models.machine import Machine
from app.models.alarm import Alarm
from app.models.ticket import Ticket
from app.models.sensor import Sensor
from app.models.user import User
from app.auth.hashing import hash_password
from datetime import datetime, timedelta
import uuid

def create_initial_roles(db: Session):
    """Create initial roles"""
    roles_data = [
        {"name": "Werker", "description": "Basic operator with limited access"},
        {"name": "Schichtleiter", "description": "Shift supervisor with operational oversight"},
        {"name": "QS", "description": "Quality assurance specialist"},
        {"name": "Datenwissenschaft", "description": "Data scientist with analytics access"},
        {"name": "Admin", "description": "System administrator with full access"}
    ]
    
    for role_data in roles_data:
        existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.add(role)
            print(f"Created role: {role_data['name']}")
    
    db.commit()

def create_initial_permissions(db: Session):
    """Create initial permissions"""
    permissions_data = [
        # Dashboard permissions
        {"name": "dashboard_view", "description": "View dashboard", "resource": "dashboard", "action": "view"},
        
        # Machine permissions
        {"name": "machines_view", "description": "View machines", "resource": "machines", "action": "view"},
        {"name": "machines_create", "description": "Create machines", "resource": "machines", "action": "create"},
        {"name": "machines_update", "description": "Update machines", "resource": "machines", "action": "update"},
        {"name": "machines_delete", "description": "Delete machines", "resource": "machines", "action": "delete"},
        
        # Alarm permissions
        {"name": "alarms_view", "description": "View alarms", "resource": "alarms", "action": "view"},
        {"name": "alarms_acknowledge", "description": "Acknowledge alarms", "resource": "alarms", "action": "acknowledge"},
        {"name": "alarms_clear", "description": "Clear alarms", "resource": "alarms", "action": "clear"},
        
        # Ticket permissions
        {"name": "tickets_view", "description": "View tickets", "resource": "tickets", "action": "view"},
        {"name": "tickets_create", "description": "Create tickets", "resource": "tickets", "action": "create"},
        {"name": "tickets_update", "description": "Update tickets", "resource": "tickets", "action": "update"},
        {"name": "tickets_assign", "description": "Assign tickets", "resource": "tickets", "action": "assign"},
        
        # Data source permissions
        {"name": "datasources_view", "description": "View data sources", "resource": "datasources", "action": "view"},
        {"name": "datasources_create", "description": "Create data sources", "resource": "datasources", "action": "create"},
        {"name": "datasources_update", "description": "Update data sources", "resource": "datasources", "action": "update"},
        {"name": "datasources_delete", "description": "Delete data sources", "resource": "datasources", "action": "delete"},
        {"name": "datasources_connect", "description": "Connect to data sources", "resource": "datasources", "action": "connect"},
        
        # Report permissions
        {"name": "reports_view", "description": "View reports", "resource": "reports", "action": "view"},
        {"name": "reports_export", "description": "Export reports", "resource": "reports", "action": "export"},
        
        # User management permissions
        {"name": "users_view", "description": "View users", "resource": "users", "action": "view"},
        {"name": "users_create", "description": "Create users", "resource": "users", "action": "create"},
        {"name": "users_update", "description": "Update users", "resource": "users", "action": "update"},
        {"name": "users_delete", "description": "Delete users", "resource": "users", "action": "delete"},
        
        # Role management permissions
        {"name": "roles_view", "description": "View roles", "resource": "roles", "action": "view"},
        {"name": "roles_create", "description": "Create roles", "resource": "roles", "action": "create"},
        {"name": "roles_update", "description": "Update roles", "resource": "roles", "action": "update"},
        {"name": "roles_delete", "description": "Delete roles", "resource": "roles", "action": "delete"},
        {"name": "roles_assign", "description": "Assign roles", "resource": "roles", "action": "assign"},
        
        # System permissions
        {"name": "system_audit", "description": "View system audit logs", "resource": "system", "action": "audit"},
        {"name": "system_config", "description": "Configure system settings", "resource": "system", "action": "config"},
    ]
    
    for perm_data in permissions_data:
        existing_perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not existing_perm:
            permission = Permission(**perm_data)
            db.add(permission)
            print(f"Created permission: {perm_data['name']}")
    
    db.commit()

def assign_permissions_to_roles(db: Session):
    """Assign permissions to roles"""
    # Get all roles and permissions
    roles = {role.name: role for role in db.query(Role).all()}
    permissions = {perm.name: perm for perm in db.query(Permission).all()}
    
    # Define role-permission mappings
    role_permissions = {
        "Werker": [
            "dashboard_view", "machines_view", "alarms_view", "tickets_view", "tickets_create"
        ],
        "Schichtleiter": [
            "dashboard_view", "machines_view", "machines_update", "alarms_view", "alarms_acknowledge",
            "tickets_view", "tickets_create", "tickets_update", "tickets_assign", "reports_view"
        ],
        "QS": [
            "dashboard_view", "machines_view", "alarms_view", "alarms_acknowledge", "tickets_view",
            "tickets_create", "tickets_update", "reports_view", "reports_export"
        ],
        "Datenwissenschaft": [
            "dashboard_view", "machines_view", "alarms_view", "tickets_view", "datasources_view",
            "datasources_create", "datasources_update", "datasources_connect", "reports_view",
            "reports_export", "system_audit"
        ],
        "Admin": [
            # Admin gets all permissions
            perm for perm in permissions.keys()
        ]
    }
    
    for role_name, perm_names in role_permissions.items():
        if role_name not in roles:
            continue
            
        role = roles[role_name]
        for perm_name in perm_names:
            if perm_name not in permissions:
                continue
                
            permission = permissions[perm_name]
            
            # Check if assignment already exists
            existing = db.query(RolePermission).filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permission.id
            ).first()
            
            if not existing:
                role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
                db.add(role_permission)
                print(f"Assigned permission {perm_name} to role {role_name}")
    
    db.commit()

def create_initial_security_policies(db: Session):
    """Create initial security policies"""
    policies_data = [
        {"policy_name": "password_policy_enabled", "policy_value": "true", "description": "Enable password policy enforcement"},
        {"policy_name": "password_min_length", "policy_value": "8", "description": "Minimum password length"},
        {"policy_name": "password_complexity", "policy_value": "true", "description": "Require complex passwords"},
        {"policy_name": "two_factor_auth", "policy_value": "false", "description": "Enable two-factor authentication"},
        {"policy_name": "session_timeout_minutes", "policy_value": "480", "description": "Session timeout in minutes (8 hours)"},
        {"policy_name": "ip_allowlist_enabled", "policy_value": "false", "description": "Enable IP allowlist"},
        {"policy_name": "max_login_attempts", "policy_value": "5", "description": "Maximum login attempts before lockout"},
        {"policy_name": "account_lockout_duration_minutes", "policy_value": "30", "description": "Account lockout duration in minutes"},
    ]
    
    for policy_data in policies_data:
        existing_policy = db.query(SecurityPolicy).filter(SecurityPolicy.policy_name == policy_data["policy_name"]).first()
        if not existing_policy:
            policy = SecurityPolicy(**policy_data)
            db.add(policy)
            print(f"Created security policy: {policy_data['policy_name']}")
    
    db.commit()

def create_sample_data_sources(db: Session):
    """Create sample data sources"""
    datasources_data = [
        {
            "name": "MQTT Broker Production",
            "protocol": "MQTT",
            "broker_url": "tcp://mqtt-broker:1883",
            "port": 1883,
            "client_id": "predictive_maintenance_client",
            "keep_alive": 60,
            "clean_session": True,
            "use_tls": False,
            "topic_filter": "sensors/+/+",
            "qos_level": 1,
            "payload_format": "JSON",
            "database_type": "InfluxDB",
            "database_host": "influxdb:8086",
            "database_name": "predictive_maintenance",
            "measurement_name": "sensor_data",
            "raw_data_retention": "30d",
            "aggregate_1min_retention": "1y",
            "aggregate_15min_retention": "5y"
        },
        {
            "name": "OPC UA Server Line 1",
            "protocol": "OPC_UA",
            "broker_url": "opc.tcp://opcua-server:4840",
            "port": 4840,
            "use_tls": False,
            "payload_format": "JSON",
            "database_type": "InfluxDB",
            "database_host": "influxdb:8086",
            "database_name": "predictive_maintenance",
            "measurement_name": "opcua_data",
            "raw_data_retention": "30d"
        },
        {
            "name": "Modbus Gateway Hall A",
            "protocol": "MODBUS",
            "database_host": "modbus-gateway",
            "port": 502,
            "payload_format": "JSON",
            "database_type": "InfluxDB",
            "database_host": "influxdb:8086",
            "database_name": "predictive_maintenance",
            "measurement_name": "modbus_data",
            "raw_data_retention": "30d"
        }
    ]
    
    for ds_data in datasources_data:
        existing_ds = db.query(DataSource).filter(DataSource.name == ds_data["name"]).first()
        if not existing_ds:
            datasource = DataSource(**ds_data)
            db.add(datasource)
            print(f"Created data source: {ds_data['name']}")
    
    db.commit()

def create_sample_machines(db: Session):
    """Create sample machines"""
    machines_data = [
        {
            "name": "Pressmaschine 1",
            "line": "L1",
            "location": "Hall A",
            "status": "running",
            "oee_percentage": 95.0,
            "anomaly_score": 0.05,
            "machine_type": "Pressmaschine",
            "manufacturer": "Schuler",
            "model": "P2H-800",
            "serial_number": "SCH-2023-001",
            "last_maintenance_date": datetime.utcnow() - timedelta(days=30),
            "next_maintenance_date": datetime.utcnow() + timedelta(days=30),
            "maintenance_interval_days": 60
        },
        {
            "name": "Pressmaschine 2",
            "line": "L2",
            "location": "Hall A",
            "status": "warning",
            "oee_percentage": 80.0,
            "anomaly_score": 0.12,
            "machine_type": "Pressmaschine",
            "manufacturer": "Schuler",
            "model": "P2H-800",
            "serial_number": "SCH-2023-002",
            "last_maintenance_date": datetime.utcnow() - timedelta(days=45),
            "next_maintenance_date": datetime.utcnow() + timedelta(days=15),
            "maintenance_interval_days": 60
        },
        {
            "name": "Extruder 1",
            "line": "L3",
            "location": "Hall B",
            "status": "warning",
            "oee_percentage": 70.0,
            "anomaly_score": 0.16,
            "machine_type": "Extruder",
            "manufacturer": "KraussMaffei",
            "model": "CX-200",
            "serial_number": "KM-2023-001",
            "last_maintenance_date": datetime.utcnow() - timedelta(days=60),
            "next_maintenance_date": datetime.utcnow() + timedelta(days=30),
            "maintenance_interval_days": 90
        },
        {
            "name": "Spritzgießmaschine",
            "line": "L3",
            "location": "Hall B",
            "status": "critical",
            "oee_percentage": 55.0,
            "anomaly_score": 0.25,
            "machine_type": "Spritzgießmaschine",
            "manufacturer": "Arburg",
            "model": "Allrounder 370S",
            "serial_number": "ARB-2023-001",
            "last_maintenance_date": datetime.utcnow() - timedelta(days=90),
            "next_maintenance_date": datetime.utcnow() + timedelta(days=7),
            "maintenance_interval_days": 90
        },
        {
            "name": "Montagelinie 1",
            "line": "L3",
            "location": "Hall C",
            "status": "running",
            "oee_percentage": 90.0,
            "anomaly_score": 0.04,
            "machine_type": "Montagelinie",
            "manufacturer": "Bosch",
            "model": "APAS",
            "serial_number": "BOS-2023-001",
            "last_maintenance_date": datetime.utcnow() - timedelta(days=15),
            "next_maintenance_date": datetime.utcnow() + timedelta(days=45),
            "maintenance_interval_days": 60
        },
        {
            "name": "Abfüllanlage",
            "line": "L2",
            "location": "Hall A",
            "status": "critical",
            "oee_percentage": 44.0,
            "anomaly_score": 0.28,
            "machine_type": "Abfüllanlage",
            "manufacturer": "Krones",
            "model": "Modulfill H",
            "serial_number": "KRO-2023-001",
            "last_maintenance_date": datetime.utcnow() - timedelta(days=120),
            "next_maintenance_date": datetime.utcnow() + timedelta(days=3),
            "maintenance_interval_days": 90
        }
    ]
    
    for machine_data in machines_data:
        existing_machine = db.query(Machine).filter(Machine.name == machine_data["name"]).first()
        if not existing_machine:
            machine = Machine(**machine_data)
            db.add(machine)
            print(f"Created machine: {machine_data['name']}")
    
    db.commit()

def create_sample_alarms(db: Session):
    """Create sample alarms"""
    # Get machines for alarm creation
    machines = db.query(Machine).all()
    if not machines:
        print("No machines found. Please create machines first.")
        return
    
    alarms_data = [
        {
            "machine_id": machines[0].id,
            "sensor_type": "temperature",
            "severity": "Kritisch",
            "message": "Temperatur zu hoch",
            "equipment_name": machines[0].name,
            "source": "Sensor",
            "threshold_value": 80.0,
            "actual_value": 85.5,
            "category": "Temperature",
            "priority": 1
        },
        {
            "machine_id": machines[1].id,
            "sensor_type": "vibration",
            "severity": "Hoch",
            "message": "Ungewöhnliche Vibration",
            "equipment_name": machines[1].name,
            "source": "Modell",
            "threshold_value": 5.0,
            "actual_value": 7.2,
            "category": "Vibration",
            "priority": 2
        },
        {
            "machine_id": machines[2].id,
            "sensor_type": "pressure",
            "severity": "Medium",
            "message": "Hoher Speicherverbrauch",
            "equipment_name": machines[2].name,
            "source": "Regel",
            "threshold_value": 10.0,
            "actual_value": 12.5,
            "category": "Pressure",
            "priority": 3
        }
    ]
    
    for alarm_data in alarms_data:
        alarm = Alarm(**alarm_data)
        db.add(alarm)
        print(f"Created alarm: {alarm_data['message']}")
    
    db.commit()

def create_sample_tickets(db: Session):
    """Create sample tickets"""
    # Get machines and alarms for ticket creation
    machines = db.query(Machine).all()
    alarms = db.query(Alarm).all()
    
    tickets_data = [
        {
            "title": "Temperatur-Sensor Kalibrierung",
            "description": "Kalibrierung des Temperatur-Sensors an Pressmaschine 1",
            "machine_id": machines[0].id if machines else None,
            "alarm_id": alarms[0].id if alarms else None,
            "status": "open",
            "ticket_type": "Maintenance",
            "priority": "High",
            "category": "Mechanical",
            "created_by": "admin@example.com",
            "estimated_duration_hours": 2.0,
            "cost_estimate": 150.0
        },
        {
            "title": "Vibrationsanalyse durchführen",
            "description": "Detaillierte Vibrationsanalyse an Pressmaschine 2",
            "machine_id": machines[1].id if machines else None,
            "alarm_id": alarms[1].id if alarms else None,
            "status": "in_progress",
            "ticket_type": "Inspection",
            "priority": "Medium",
            "category": "Mechanical",
            "assignee": "technician@example.com",
            "created_by": "admin@example.com",
            "estimated_duration_hours": 4.0,
            "cost_estimate": 300.0
        },
        {
            "title": "Druckregelung überprüfen",
            "description": "Überprüfung der Druckregelung am Extruder 1",
            "machine_id": machines[2].id if machines else None,
            "alarm_id": alarms[2].id if alarms else None,
            "status": "done",
            "ticket_type": "Repair",
            "priority": "Low",
            "category": "Electrical",
            "assignee": "technician@example.com",
            "created_by": "admin@example.com",
            "completed_by": "technician@example.com",
            "estimated_duration_hours": 1.5,
            "actual_duration_hours": 1.2,
            "cost_estimate": 200.0,
            "actual_cost": 180.0
        }
    ]
    
    for ticket_data in tickets_data:
        ticket = Ticket(**ticket_data)
        db.add(ticket)
        print(f"Created ticket: {ticket_data['title']}")
    
    db.commit()

def create_admin_user(db: Session):
    """Create admin user if not exists"""
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        admin_user = User(
            email="admin@example.com",
            full_name="System Administrator",
            hashed_password=hash_password("admin123"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("Created admin user: admin@example.com")
    else:
        print("Admin user already exists")

def main():
    """Main seeding function"""
    print("Starting Phase 2 database seeding...")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create initial data
        create_admin_user(db)
        create_initial_roles(db)
        create_initial_permissions(db)
        assign_permissions_to_roles(db)
        create_initial_security_policies(db)
        create_sample_data_sources(db)
        create_sample_machines(db)
        create_sample_alarms(db)
        create_sample_tickets(db)
        
        print("\nPhase 2 database seeding completed successfully!")
        print("\nDefault admin credentials:")
        print("Email: admin@example.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
