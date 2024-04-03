#! /usr/bin/env sh
set -e

# Run migrations
alembic upgrade head

# Run with uvicorn
exec uvicorn --reload --host 0.0.0.0 --port 8000 "app.main:app"
