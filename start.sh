#!/bin/bash
set -e

# Извлекаем компоненты из DATABASE_URL
DB_USER=$(echo $DATABASE_URL | awk -F'[:/@]' '{print $4}')
DB_PASSWORD=$(echo $DATABASE_URL | awk -F'[:/@]' '{print $5}')
DB_HOST=$(echo $DATABASE_URL | awk -F'[:/@]' '{print $6}')
DB_PORT=$(echo $DATABASE_URL | awk -F'[:/@]' '{print $7}')
DB_NAME=$(echo $DATABASE_URL | awk -F'/' '{print $4}')

# Ожидаем доступности базы данных
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Waiting for database..."
  sleep 2
done

# Устанавливаем пароль для psql
export PGPASSWORD=$DB_PASSWORD

# Проверяем, существует ли база данных, и создаем ее, если нет
psql -h "$DB_HOST" -U "$DB_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || psql -h "$DB_HOST" -U "$DB_USER" -c "CREATE DATABASE $DB_NAME"

# Применяем миграции Alembic
alembic upgrade head

# Запускаем приложение
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.main:app