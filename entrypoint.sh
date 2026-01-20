#!/usr/bin/env sh
set -e

echo "➡️ Rodando migrations..."
alembic upgrade head

echo "🚀 Iniciando API..."
exec "$@"
