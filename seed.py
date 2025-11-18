#!/usr/bin/env python3
"""
Script to seed the database with initial data for the predictive maintenance backend.
"""

import sys
import os

# Add the current directory to the path
sys.path.append('.')

from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models import User, Machine, Sensor, Alarm, Ticket
from app.api.core.security import get_password_hash

def seed():
    db = SessionLocal()

    try:
        # Create users (idempotent)
        admin = db.query(User).filter_by(email="admin@example.com").first()
        if not admin:
            admin = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role="admin",
            )
            db.add(admin)

        user1 = db.query(User).filter_by(email="user1@example.com").first()
        if not user1:
            user1 = User(
                email="user1@example.com",
                hashed_password=get_password_hash("user123"),
                full_name="User One",
                role="operator",
            )
            db.add(user1)

        # Create machines (idempotent)
        machine1 = db.query(Machine).filter_by(name="Machine A").first()
        if not machine1:
            machine1 = Machine(
                name="Machine A",
                line="Line 1",
                location="Factory 1",
            )
            db.add(machine1)

        machine2 = db.query(Machine).filter_by(name="Machine B").first()
        if not machine2:
            machine2 = Machine(
                name="Machine B",
                line="Line 2",
                location="Factory 1",
            )
            db.add(machine2)

        db.commit()  # Commit to get IDs / existing instances

        # Create sensors
        # Create sensors (idempotent by machine + sensor_type)
        def get_sensor(machine, sensor_type):
            return (
                db.query(Sensor)
                .filter_by(machine_id=machine.id, sensor_type=sensor_type)
                .first()
            )

        if machine1:
            if not get_sensor(machine1, "temperature"):
                sensor1 = Sensor(
                    machine_id=machine1.id,
                    sensor_type="temperature",
                    unit="C",
                    min_threshold=20.0,
                    max_threshold=80.0,
                )
                db.add(sensor1)
            if not get_sensor(machine1, "vibration"):
                sensor2 = Sensor(
                    machine_id=machine1.id,
                    sensor_type="vibration",
                    unit="mm/s",
                    min_threshold=0.0,
                    max_threshold=10.0,
                )
                db.add(sensor2)

        if machine2 and not get_sensor(machine2, "pressure"):
            sensor3 = Sensor(
                machine_id=machine2.id,
                sensor_type="pressure",
                unit="bar",
                min_threshold=1.0,
                max_threshold=5.0,
            )
            db.add(sensor3)

        db.commit()

        # Create alarms (one sample alarm for Machine A temperature)
        alarm1 = (
            db.query(Alarm)
            .filter_by(machine_id=machine1.id, sensor_type="temperature")
            .first()
            if machine1
            else None
        )
        if machine1 and not alarm1:
            alarm1 = Alarm(
                machine_id=machine1.id,
                sensor_type="temperature",
                severity="high",
                message="High temperature detected",
            )
            db.add(alarm1)
            db.commit()

        # Create tickets linked to that alarm
        if alarm1:
            ticket1 = (
                db.query(Ticket)
                .filter_by(
                    machine_id=machine1.id,
                    alarm_id=alarm1.id,
                    title="Maintenance Required",
                )
                .first()
            )
            if not ticket1:
                ticket1 = Ticket(
                    machine_id=machine1.id,
                    title="Maintenance Required",
                    description="Check temperature sensor",
                    status="open",
                    alarm_id=alarm1.id,
                )
                db.add(ticket1)
                db.commit()

        print("Database seeded successfully!")

    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error during seeding (likely duplicates, safe to ignore): {e}")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
