#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

python manage.py add_user quyviet viet.info.43@gmail.com 12345678

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
