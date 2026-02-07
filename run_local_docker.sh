#!/bin/bash

# Define variables
IMAGE_NAME="gender-school-local"
CONTAINER_NAME="gender-school-container"

echo "🧹 Cleaning up old resources..."
# Stop and remove existing container
docker stop $CONTAINER_NAME 2>/dev/null
docker rm $CONTAINER_NAME 2>/dev/null

# Remove dangling images (failed builds or replaced images) to free space
echo "🗑️ Removing dangling images..."
docker image prune -f

echo "🚀 Building Docker image..."
docker build -t $IMAGE_NAME .

if [ $? -ne 0 ]; then
    echo "❌ Build failed! Aborting."
    exit 1
fi
echo "✅ Build successful!"

echo "🧪 Running tests inside the container..."
# Run Django tests inside a temporary container using the image we just built
docker run --rm \
    -e SECRET_KEY=test-key \
    -e DATABASE_URL=sqlite:///db.sqlite3 \
    $IMAGE_NAME \
    python manage.py test

# Check if tests passed
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Aborting deployment."
    exit 1
fi
echo "✅ All tests passed!"

echo "🏃 Starting application container..."
echo "🌍 App will be available at http://localhost:8080"
echo "📝 Use Ctrl+C to stop the server"

# Run the actual server
docker run --name $CONTAINER_NAME \
    --rm \
    -p 8080:8080 \
    -e DEBUG=True \
    -e SECRET_KEY=django-insecure-local-dev-key \
    -e ALLOWED_HOSTS=* \
    -e DATABASE_URL=sqlite:///db.sqlite3 \
    $IMAGE_NAME
