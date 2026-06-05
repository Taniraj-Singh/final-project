#!/usr/bin/env bash
set -euo pipefail

cd /app

python -m pytest tests/test_hysteresis.py -v --tb=short --no-header -p no:cacheprovider 2>&1
