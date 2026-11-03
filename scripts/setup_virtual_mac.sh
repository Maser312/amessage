#!/usr/bin/env bash
set -e
echo "=== AMessage Virtual Mac & Relay Installer ==="
if ! command -v docker &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y docker.io docker-compose
fi
docker-compose -f "$(dirname "$0")/../docker-compose.yml" up -d --build
echo "=== Setup Complete! Relay on port 8080 ==="
