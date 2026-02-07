#!/bin/bash

# Define variables
IMAGE_NAME="gender-school-local"
CONTAINER_NAME="gender-school-container"

echo "🧹 Cleaning up old resources..."

# 1. Stop and remove ALL Docker containers (as requested)
echo "🛑 Stopping and Removing ALL containers..."
# Use xargs -r to avoid errors if no containers exist. -f forces removal (stops if running).
docker ps -aq | xargs -r docker rm -f

# 2. Skip aggressive PID killing on port 8080 to avoid killing Docker daemon itself.
# If port is still busy, it's likely Docker holding it, which will be reused.
echo "✅ Cleanup complete."

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
docker run --rm     -e SECRET_KEY=test-key     -e DATABASE_URL=sqlite:///db.sqlite3     $IMAGE_NAME     python manage.py test

# Check if tests passed
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Aborting deployment."
    exit 1
fi
echo "✅ All tests passed!"

echo "🏃 Starting application container..."
echo "🌍 App will be available at http://localhost:8080"
echo "📝 Use Ctrl+C to stop the server"

# Load variables from .env if it exists
ENV_ARGS=""
if [ -f backend/.env ]; then
    echo "📄 Loading configuration from backend/.env..."
    # Read .env file line by line
    while IFS= read -r line || [[ -n "$line" ]]; do
      # Skip empty lines and comments
      if [[ -z "$line" ]] || [[ "$line" =~ ^# ]]; then
        continue
      fi
      # Pass variable to Docker
      ENV_ARGS="$ENV_ARGS -e $line"
    done < backend/.env
else
    echo "⚠️ No .env file found. Using default SQLite configuration."
    ENV_ARGS="-e DEBUG=True -e SECRET_KEY=django-insecure-local-dev-key -e ALLOWED_HOSTS=* -e DATABASE_URL=sqlite:///db.sqlite3"
fi

# Prepare volumes and credentials
mkdir -p backend/media
VOLUME_ARGS="-v $(pwd)/backend/media:/app/media"
CREDENTIALS_OVERRIDE=""

if [ -f backend/.env ]; then
    # Extract path from .env (handle potential quotes)
    GCP_KEY_HOST_PATH=$(grep "^GOOGLE_APPLICATION_CREDENTIALS=" backend/.env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
    
    if [ -n "$GCP_KEY_HOST_PATH" ]; then
        if [ -f "$GCP_KEY_HOST_PATH" ]; then
            echo "🔑 Found GCP Credentials at $GCP_KEY_HOST_PATH"
            VOLUME_ARGS="$VOLUME_ARGS -v $GCP_KEY_HOST_PATH:/app/credentials.json:ro"
            CREDENTIALS_OVERRIDE="-e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json"
        else
            echo "⚠️ GCP Credentials configured in .env but file not found at: $GCP_KEY_HOST_PATH"
        fi
    fi
fi

# Run the actual server
docker run --name $CONTAINER_NAME \
    --rm \
    -p 8080:8080 \
    $ENV_ARGS \
    $CREDENTIALS_OVERRIDE \
    $VOLUME_ARGS \
    $IMAGE_NAME
