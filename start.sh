#!/bin/bash

until pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for database..."
  sleep 2
done


export PGPASSWORD=postgres

psql -h db -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'fittest'" | grep -q 1 || psql -h db -U postgres -c "CREATE DATABASE fittest"

export SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@db:5432/fittest"

export PYTHONPATH=/app:$PYTHONPATH

alembic upgrade head

gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.main:app