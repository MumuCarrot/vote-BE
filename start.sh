#!/bin/sh
set -e
echo "Running database migrations..."
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
echo "Starting FastAPI server..."
exec python -m app.main
