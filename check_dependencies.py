import importlib
import sys

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: {e}")
        return False

print("🔍 Checking required dependencies...")
print("=" * 50)

required_modules = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "alembic", 
    "psycopg2",
    "passlib",
    "bcrypt",
    "jose",
    "pydantic",
    "pydantic_settings",
    "numpy",
    "pandas",
    "sklearn",
    "scipy",
    "joblib",
    "paho.mqtt",
    "dotenv"
]

all_ok = True
for module in required_modules:
    if not check_module(module):
        all_ok = False

print("=" * 50)
if all_ok:
    print("🎉 All dependencies are installed!")
else:
    print("🔧 Some dependencies are missing. Run: pip install -r requirements.txt")