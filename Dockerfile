FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies (all pinned in requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY buffer.py .
COPY features.py .
COPY hysteresis.py .
COPY model_manager.py .
COPY pca_monitor.py .
COPY train_model.py .
COPY main.py .
COPY mqtt_enterprise_bridge.py .
COPY mqtt_enterprise_simulator.py .

# Create model directory
RUN mkdir -p /app/models

# Expose AI monitoring service port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
