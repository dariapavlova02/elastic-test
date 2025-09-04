#!/bin/bash

echo "🔧 Fixing AI service on server..."

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull

# Stop current containers
echo "🛑 Stopping current containers..."
docker-compose -f docker-compose.simple.yml down

# Remove old image to force rebuild
echo "🗑️ Removing old server image..."
docker rmi elastic-test_server_api 2>/dev/null || true

# Rebuild and start containers
echo "🔨 Rebuilding and starting containers..."
docker-compose -f docker-compose.simple.yml up -d --build

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Test AI service
echo "🧪 Testing AI service..."
curl -X POST http://localhost/search -H "Content-Type: application/json" -d '{"query": "Петро Порошенко", "limit": 1}' | jq '.server_info'

echo "✅ Done! Check the output above for AI service status."
