import os

required_files = [
    'requirements.txt',
    'alembic.ini',
    'app/main.py',
    'app/models/__init__.py',
    'main.py',
    'models/isolation_forest.pkl',
    'models/scaler.pkl',
    'seed.py',
    'seed_phase2.py'
]

print("🔍 Checking required files...")
print("=" * 50)

missing_files = []
for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING")
        missing_files.append(file)

print("=" * 50)
if missing_files:
    print(f"⚠️  Missing {len(missing_files)} files. Please check:")
    for file in missing_files:
        print(f"   - {file}")
else:
    print("🎉 All required files found!")