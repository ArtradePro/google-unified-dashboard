#!/bin/bash

# Google Unified Dashboard Setup Script
# This script helps set up the dashboard environment

set -e

echo "=========================================="
echo "Google Unified Dashboard Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.8 or higher is required"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed successfully"

# Setup environment file
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created. Please edit it with your API keys."
else
    echo ".env file already exists"
fi

# Check for service account file
echo ""
if [ ! -f "service-account.json" ]; then
    echo "⚠️  WARNING: service-account.json not found"
    echo "   Please follow these steps to set up Google Sheets API:"
    echo "   1. Go to https://console.cloud.google.com/"
    echo "   2. Create a new project or select existing"
    echo "   3. Enable Google Sheets API and Google Drive API"
    echo "   4. Create a Service Account"
    echo "   5. Download the JSON key file"
    echo "   6. Save it as 'service-account.json' in this directory"
    echo ""
else
    echo "✓ service-account.json found"
fi

# Summary
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. If not done, add your service-account.json file"
echo ""
echo "3. Customize config.yaml if needed:"
echo "   nano config.yaml"
echo ""
echo "4. Run the dashboard:"
echo "   python main.py"
echo ""
echo "5. Set up Looker Studio visualization:"
echo "   See LOOKER_STUDIO_SETUP.md for instructions"
echo ""
echo "=========================================="
