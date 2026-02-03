#!/bin/bash
# Shell script to set up virtual environment for Linux/macOS
# Run this script: chmod +x setup_venv.sh && ./setup_venv.sh

echo "Setting up virtual environment..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Virtual environment setup complete!"
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the application:"
echo "  uvicorn app.main:app --reload"
