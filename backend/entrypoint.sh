#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# If arguments are provided (e.g., python manage.py test), execute them
if [ "$#" -gt 0 ]; then
    exec "$@"
fi

# Default behavior: Run migrations and start Gunicorn
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Creating default superuser (admin/admin)..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo "Starting Gunicorn..."
exec gunicorn school_project.wsgi:application --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 60
