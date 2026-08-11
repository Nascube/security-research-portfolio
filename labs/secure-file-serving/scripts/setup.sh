#!/bin/bash
# Setup script for the Secure File Serving Lab

set -e

echo "=== Secure File Serving Lab - Setup ==="
echo ""

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "✓ Python $(python3 --version) found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create fixtures directory if it doesn't exist
mkdir -p fixtures

# Run tests
echo ""
echo "Running tests..."
pytest tests/ -v

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To run the Flask application:"
echo "  python -m src.app"
echo ""
echo "To run tests:"
echo "  pytest tests/"
echo ""
echo "To build and run with Docker:"
echo "  docker-compose build"
echo "  docker-compose up"
echo ""
