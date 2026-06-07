#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "=== Task Manager Setup ==="
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[1/4] Virtual environment exists, skipping..."
fi

# Activate and install dependencies
echo "[2/4] Installing dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt

# Copy .env if not exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "[3/4] Created .env from .env.example"
    else
        echo "[3/4] No .env.example found, using defaults"
    fi
else
    echo "[3/4] .env already exists, skipping..."
fi

# Seed database with test data
echo "[4/4] Seeding database with test data..."
python3 seed.py

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Then open http://localhost:5000"
echo ""
echo "For email testing, install Mailpit:"
echo "  https://mailpit.axllent.org"
echo "  Mailpit UI: http://localhost:8025"
