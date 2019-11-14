#!/bin/bash
set -e
set +x

# Source any relevant environment variables

if [ "$1" = 'web' ]; then
  # If you need to run migrations
  # /app/setup_alembic.sh
  exec gunicorn -b 0.0.0.0:5000 -w 4 example.web.app:app
elif [ "$1" = 'celery' ]; then
  exec celery -A example.worker.celery worker -l info -Q default
else
  exec "${@}"
fi