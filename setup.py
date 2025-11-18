import os
import sys

def create_file(filename, content):
    """Create a file with the given content"""
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created: {filename}")
    else:
        print(f"📁 Already exists: {filename}")

def main():
    print("🚀 Creating Docker Setup Files...")
    print("=" * 50)
    
    # Create docker-compose.db.yml
    db_compose_content = '''version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: predictive_maintenance
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: "awaisAWM#2002"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
'''
    create_file('docker-compose.db.yml', db_compose_content)
    
    # Create docker-compose.full.yml
    full_compose_content = '''version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: predictive_maintenance
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: "awaisAWM#2002"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:awaisAWM%232002@db:5432/predictive_maintenance
      - JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    command: >
      sh -c "sleep 10 && 
             alembic upgrade head && 
             python seed.py && 
             python seed_phase2.py &&
             uvicorn app.main:app --host 0.0.0.0 --port 8000"

  ai:
    build: .
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://postgres:awaisAWM%232002@db:5432/predictive_maintenance
      - MQTT_BROKER=broker.hivemq.com
    depends_on:
      - db
      - backend
    volumes:
      - .:/app
    command: >
      sh -c "sleep 20 && 
             python main.py"

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  postgres_data:
'''
    create_file('docker-compose.full.yml', full_compose_content)
    
    # Create .env file
    env_content = '''DATABASE_URL=postgresql://postgres:awaisAWM%232002@localhost:5432/predictive_maintenance
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
LOG_LEVEL=INFO
MQTT_BROKER=broker.hivemq.com
MQTT_PORT=1883
MODEL_PATH=./models
'''
    create_file('.env', env_content)
    
    print("=" * 50)
    print("🎉 All files created successfully!")
    print("\n📋 Next commands to run:")
    print("1. docker-compose -f docker-compose.db.yml up -d")
    print("2. docker-compose -f docker-compose.full.yml up --build -d")
    print("3. python verify_setup.py")

if __name__ == "__main__":
    main()