# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build Backend and Serve
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend

# Create directory for static files source
RUN mkdir -p backend/static

# Copy frontend build artifacts
COPY --from=frontend-build /app/frontend/dist/index.html /app/backend/templates/index.html
COPY --from=frontend-build /app/frontend/dist/assets /app/backend/static/assets
COPY --from=frontend-build /app/frontend/dist/vite.svg /app/backend/static/

WORKDIR /app/backend

# Collect static files
# We use dummy values for build time only, they are not persisted in the final image ENV
RUN SECRET_KEY=dummy_build_key DATABASE_URL=sqlite:///db.sqlite3 python manage.py collectstatic --noinput

# Copy entrypoint script and make it executable
COPY backend/entrypoint.sh /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

# Expose port
EXPOSE 8080

# Use entrypoint script to run migrations and start server
ENTRYPOINT ["/app/backend/entrypoint.sh"]
