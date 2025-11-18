import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Quick model training
print("🤖 Training quick model...")
X_train = np.random.normal(0, 1, (1000, 10))
model = IsolationForest(random_state=42)
model.fit(X_train)

scaler = StandardScaler()
scaler.fit(X_train)

os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/isolation_forest.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("✅ Quick models saved! Now run your main.py again.")