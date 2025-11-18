import requests
import time
import psycopg2

def test_database():
    print("🧪 Testing Database Connection...")
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="predictive_maintenance", 
            user="postgres",
            password="awaisAWM#2002",
            port="5432"
        )
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        print(f"✅ Database: Connected (Found {len(tables)} tables)")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database: {e}")
        return False

def test_service(url, name, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: RUNNING")
            return True
        else:
            print(f"⚠️  {name}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

def main():
    print("🚀 COMPLETE SYSTEM TEST")
    print("=" * 60)
    
    # Test database first
    db_ok = test_database()
    
    # Wait a bit for services to start
    if db_ok:
        print("\n⏳ Waiting for services to start...")
        time.sleep(10)
    
    # Test services
    services = [
        ("Backend API", "http://localhost:8000/health"),
        ("Backend Docs", "http://localhost:8000/docs"),
        ("AI Monitoring", "http://localhost:8001/health"),
        ("AI Dashboard", "http://localhost:8001/dashboard")
    ]
    
    print("\n🧪 Testing Services...")
    all_services_ok = True
    for name, url in services:
        if not test_service(url, name, timeout=15):
            all_services_ok = False
        time.sleep(2)
    
    print("=" * 60)
    if db_ok and all_services_ok:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n📊 ACCESS POINTS:")
        print("   Backend API:    http://localhost:8000")
        print("   API Docs:       http://localhost:8000/docs")
        print("   AI Dashboard:   http://localhost:8001/dashboard") 
        print("   pgAdmin:        http://localhost:5050")
        print("   Database:       localhost:5432")
    else:
        print("🔧 Some components need attention.")
        print("\n📋 TROUBLESHOOTING:")
        print("   1. Check logs: docker-compose -f docker-compose.full.yml logs")
        print("   2. Check individual: docker-compose -f docker-compose.full.yml logs [service]")
        print("   3. Restart services: docker-compose -f docker-compose.full.yml restart")

if __name__ == "__main__":
    main()