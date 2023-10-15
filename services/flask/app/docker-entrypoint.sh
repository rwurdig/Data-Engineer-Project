#!/bin/sh

set -e

# Log that the entrypoint script is running
echo "Running docker-entrypoint.sh..."

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start the Flask application using Gunicorn
echo "Starting Flask application..."
gunicorn -c gunicorn.config.py wsgi:app
