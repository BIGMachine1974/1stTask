#!/bin/bash
# First-time setup for Replit deployment
set -e

echo "=== Agent Team: Chief of Staff — Replit Setup ==="

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -e ".[google,pdf]"

# Install frontend dependencies and build
echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Create static file directory for serving frontend from backend
echo "Setting up static file serving..."
mkdir -p backend/static
cp -r frontend/dist/* backend/static/

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Add your ANTHROPIC_API_KEY in the Secrets tab (lock icon in sidebar)"
echo "  2. Click Run to start the server"
echo "  3. For Google Workspace: add GOOGLE_CREDENTIALS as a secret (JSON contents of credentials.json)"
echo ""
