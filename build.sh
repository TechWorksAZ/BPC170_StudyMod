#!/usr/bin/env bash
# Build script for Render deployment
echo "Building application..."

# Install dependencies
pip install -r requirements.txt

# Populate database
echo "Populating database..."
python data/populate_db.py

echo "Build complete!"

