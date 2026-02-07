#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn school_project.wsgi:application --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 60
