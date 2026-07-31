#!/bin/sh
set -eu

# Ensure media and logs directories exist (static files are baked in at build time)
mkdir -p /app/media/catalog /app/logs

# --- Wait for postgres with a bounded timeout ---
echo "Waiting for postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}..."
timeout=30
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT" || [ "$timeout" -le 0 ]; do
  timeout=$((timeout - 1))
  sleep 1
done

if [ "$timeout" -le 0 ]; then
  echo "ERROR: PostgreSQL did not become reachable within 30s" >&2
  exit 1
fi
echo "PostgreSQL is reachable."

# Running migrations
echo "Running migrations..."
python manage.py migrate --noinput

# --- Superuser bootstrap: idempotent, but guard against a duplicate-create race ---
echo "Ensuring superuser exists..."
if ! python manage.py init_admin; then
  echo "WARNING: init_admin failed (possible race with another replica or existing user). Continuing." >&2
fi

# collectstatic is done at image build time now (see Dockerfile) — not here.

echo "Starting application..."
exec "$@"