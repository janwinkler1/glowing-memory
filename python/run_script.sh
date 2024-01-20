#!/bin/bash
echo "Running script at $(date)" >> /var/log/script.log

# Export all environment variables
export $(cat /app/.env | xargs) && echo "Environment variables loaded"

# Run Python script
/usr/local/bin/python3 /app/main.py >> /var/log/script.log 2>&1
