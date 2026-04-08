#!/usr/bin/env pwsh
# Post-create setup script for the dev container

# Install uv (Python package manager)
Write-Host "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH for this session
$env:PATH = "$HOME/.local/bin:$env:PATH"

# Sync Python dependencies
Write-Host "Syncing Python dependencies..."
uv sync

Write-Host "Post-create setup complete!"
