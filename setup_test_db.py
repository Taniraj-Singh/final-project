#!/usr/bin/env python3
"""
Script to set up the test database for the predictive maintenance backend.
This script creates a test database and user for running tests.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_test_database():
    """Create the test database and user"""

    # Database connection parameters
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = 'postgres'  # Connect to default postgres database first
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Create test user if it doesn't exist
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'test_user') THEN
                    CREATE USER test_user WITH PASSWORD 'test_password';
                END IF;
            END
            $$;
        """)

        # Create test database if it doesn't exist
        cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = 'test_db'
        """)
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE test_db OWNER test_user")
            print("Created test database 'test_db'")
        else:
            print("Test database 'test_db' already exists")

        # Grant permissions
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user")

        # Enable UUID extension in test database
        cursor.execute("GRANT test_user TO postgres")
        cursor.execute("\\c test_db")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"timescaledb\"")

        cursor.close()
        conn.close()

        print("Test database setup completed successfully!")
        print("You can now run tests with: pytest tests/test_alarms.py -v")

    except psycopg2.Error as e:
        print(f"Error setting up test database: {e}")
        print("Make sure PostgreSQL is running and you have the correct credentials.")
        sys.exit(1)

if __name__ == "__main__":
    create_test_database()
