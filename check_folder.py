import os
import sys
from pathlib import Path

def check_folder_structure():
    print("🔍 ANALYZING YOUR FOLDER STRUCTURE...")
    print("=" * 60)
    
    current_dir = Path(".").absolute()
    print(f"📁 Current Directory: {current_dir}")
    print("=" * 60)
    
    # Count files by type
    file_types = {}
    python_files = []
    all_files = []
    
    for root, dirs, files in os.walk("."):
        for file in files:
            file_path = Path(root) / file
            all_files.append(file_path)
            
            # Get file extension
            ext = file_path.suffix.lower()
            file_types[ext] = file_types.get(ext, 0) + 1
            
            # Track Python files
            if ext == '.py':
                python_files.append(file_path)
    
    print("📊 FILE TYPE SUMMARY:")
    for ext, count in sorted(file_types.items()):
        print(f"   {ext or 'no extension'}: {count} files")
    
    print(f"\n🐍 PYTHON FILES ({len(python_files)} found):")
    for py_file in python_files:
        file_size = py_file.stat().st_size if py_file.exists() else 0
        print(f"   📄 {py_file} ({file_size} bytes)")
        
        # Read first few lines to identify the file
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                first_lines = [f.readline().strip() for _ in range(5)]
            
            # Check for clues about what the file does
            content = ' '.join(first_lines).lower()
            if 'fastapi' in content:
                print("      🚀 FastAPI Application")
            if 'mqtt' in content:
                print("      📡 MQTT Client")
            if 'predict' in content or 'anomaly' in content:
                print("      🤖 AI Prediction System")
            if 'database' in content or 'sql' in content:
                print("      🗄️ Database Operations")
            if 'backend' in content:
                print("      ⚙️ Backend System")
                
        except Exception as e:
            print(f"      ❌ Could not read: {e}")
    
    print(f"\n📋 ALL FILES ({len(all_files)} total):")
    for file_path in sorted(all_files):
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"   {'📄' if file_path.suffix == '.py' else '📝'} {file_path} ({size} bytes)")
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATIONS:")
    
    # Check for potential issues
    main_files = [f for f in python_files if 'main' in f.name.lower()]
    if len(main_files) > 1:
        print("⚠️  Multiple main.py files detected - we need to identify which is AI and which is backend")
    
    if not any('main.py' in str(f) for f in python_files):
        print("⚠️  No main.py found - we need to identify the entry point")
    
    print("✅ Run this script to see what you're working with!")

def find_main_files():
    """Specifically look for main files and analyze them"""
    print("\n🔎 LOOKING FOR MAIN FILES...")
    print("=" * 50)
    
    main_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if 'main' in file.lower() and file.endswith('.py'):
                main_files.append(Path(root) / file)
    
    if not main_files:
        print("❌ No main.py files found!")
        return
    
    for main_file in main_files:
        print(f"\n📄 Analyzing: {main_file}")
        print("-" * 40)
        
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Analyze the file
            print(f"   Size: {len(content)} characters, {len(lines)} lines")
            
            # Check for key indicators
            indicators = {
                'FastAPI': 'fastapi' in content.lower(),
                'MQTT': 'mqtt' in content.lower(),
                'Anomaly Detection': any(word in content.lower() for word in ['anomaly', 'predict', 'detect']),
                'Database': any(word in content.lower() for word in ['database', 'sql', 'postgres']),
                'Backend API': any(word in content.lower() for word in ['backend', 'api', 'endpoint', 'route']),
                'WebSocket': 'websocket' in content.lower(),
                'Dashboard': 'dashboard' in content.lower(),
            }
            
            print("   Features detected:")
            for feature, detected in indicators.items():
                if detected:
                    print(f"      ✅ {feature}")
            
            # Try to identify the type
            if 'fastapi' in content.lower() and 'mqtt' in content.lower():
                print("   🎯 TYPE: AI Factory Monitoring System")
            elif 'fastapi' in content.lower() and 'database' in content.lower():
                print("   🎯 TYPE: Backend API System")
            else:
                print("   🎯 TYPE: Unknown - need manual inspection")
                
            # Show first 3 lines for identification
            print("   First few lines:")
            for i, line in enumerate(lines[:3]):
                if line.strip():
                    print(f"      {i+1}: {line.strip()}")
                    
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")

if __name__ == "__main__":
    check_folder_structure()
    find_main_files()
    
    print("\n" + "=" * 60)
    print("📝 NEXT STEPS:")
    print("1. Run this script: python check_folder.py")
    print("2. Share the output with me")
    print("3. I'll tell you exactly which files to use and how to proceed!")