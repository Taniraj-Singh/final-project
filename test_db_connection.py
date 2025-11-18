import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="predictive_maintenance",
        user="postgres",
        password="awaisAWM#2002",
        port="5432"
    )
    print("✅ Database connected successfully!")
    
    # Test basic query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ PostgreSQL Version: {version[0]}")
    
    # List databases
    cursor.execute("SELECT datname FROM pg_database;")
    databases = cursor.fetchall()
    print("✅ Available databases:", [db[0] for db in databases])
    
    conn.close()
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")