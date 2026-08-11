#!/bin/bash
# Teardown script for the Secure File Serving Lab

set -e

echo "=== Secure File Serving Lab - Teardown ==="
echo ""

# Stop Docker containers if running
if command -v docker-compose &> /dev/null; then
    if docker-compose ps &> /dev/null; then
        echo "Stopping Docker containers..."
        docker-compose down || true
    fi
fi

# Remove virtual environment
if [ -d "venv" ]; then
    echo "Removing virtual environment..."
    rm -rf venv
fi

# Remove Python cache
echo "Removing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

# Remove pytest cache
rm -rf .pytest_cache .coverage htmlcov

echo ""
echo "=== Teardown Complete ==="
echo ""
