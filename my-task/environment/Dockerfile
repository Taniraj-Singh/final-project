# IMPORTANT: Replace the FROM line with the exact approved repo image reference
# shown on the Silver repo page — copy it verbatim, e.g.:
#   FROM ghcr.io/afterquery/silver-repo-abc123:latest
# The line below is a placeholder that will fail the image-build stage.
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install only what's needed to run the hysteresis tests
RUN pip install --no-cache-dir \
    pytest==8.2.2

COPY . .
