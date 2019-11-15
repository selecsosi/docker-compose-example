#!/usr/bin/env bash

until psql -h postgres -U postgres -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

psql -h postgres -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'db_name'" |\
    grep -q 1 ||\
    psql -h postgres -U postgres -c "CREATE DATABASE db_name"

# Enable required extensions by application
psql -h postgres -U postgres -d postgres -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

cd /app/example
alembic upgrade head
cd /app