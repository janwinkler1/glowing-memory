#!/bin/bash
echo "=== Running script at $(date) ==="

# Source environment variables (written at container startup)
set -a
source /etc/environment
set +a
echo "Environment variables loaded"

# Run Python script with unbuffered output
/app/.venv/bin/python -u /app/src/main.py 2>&1
