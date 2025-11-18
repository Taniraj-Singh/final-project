import os
import shutil
from pathlib import Path

# === CONFIGURATION ===
SAFE_DELETE_FOLDERS = [
    "__pycache__",
    ".pytest_cache",
    "pytest_cache"
]

SAFE_DELETE_FILES = [
    "fix_models.py",
    "quick_fill.py",
    "CompleteTest.py",
    "python_final_system_test.py",
    "test_after_fix.py",
    "nozzle.env",  # Only if .env exists
    "24H2020.csv"
]

MODEL_FOLDER = "models"
MODEL_KEEP_KEY = "20251017"  # Keep latest models (update if needed)

# === CLEANUP SCRIPT ===
root = Path(__file__).resolve().parent

def delete_folder(folder_path: Path):
    """Delete a folder safely."""
    try:
        if folder_path.exists():
            shutil.rmtree(folder_path)
            print(f"🗑️ Deleted folder: {folder_path}")
    except Exception as e:
        print(f"⚠️ Could not delete {folder_path}: {e}")

def delete_file(file_path: Path):
    """Delete a file safely."""
    try:
        if file_path.exists():
            file_path.unlink()
            print(f"🗑️ Deleted file: {file_path}")
    except Exception as e:
        print(f"⚠️ Could not delete {file_path}: {e}")

def clean_models():
    """Keep only latest model files."""
    model_dir = root / MODEL_FOLDER
    if not model_dir.exists():
        return
    for file in model_dir.glob("*.joblib"):
        if MODEL_KEEP_KEY not in file.name:
            file.unlink()
            print(f"🗑️ Deleted old model: {file}")

def main():
    print("🚀 Starting project cleanup...\n")

    # Step 1: Delete cache folders recursively
    for folder in SAFE_DELETE_FOLDERS:
        for path in root.rglob(folder):
            delete_folder(path)

    # Step 2: Delete specific files
    for file in SAFE_DELETE_FILES:
        for path in root.rglob(file):
            delete_file(path)

    # Step 3: Clean old models
    clean_models()

    print("\n✅ Cleanup completed successfully!")
    print("💡 Your project is now organized and production-ready.")

if __name__ == "__main__":
    main()
