# --- Stage 1: Build virtual environment ---
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
# Prefer: pip install --require-hashes -r requirements.txt (pip-compile --generate-hashes)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Final runtime image ---
FROM python:3.12-slim AS runner
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings \
    HOME=/home/django
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    tini \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

RUN addgroup --system --gid 1000 django && \
    adduser --system --uid 1000 --gid 1000 --home /home/django --shell /usr/sbin/nologin django && \
    mkdir -p /home/django && \
    chown django:django /home/django

RUN mkdir -p /app/staticfiles /app/media/catalog /app/logs && \
    chown -R django:django /app

COPY --chown=django:django . .
COPY --chown=django:django scripts/entrypoint.sh ./scripts/
RUN chmod +x ./scripts/entrypoint.sh

# --- Build-time static collection ---
# SECRET_KEY and FRONTEND_URL here are throwaway values scoped to this single
# RUN layer only — needed purely so settings.py imports cleanly during
# collectstatic. Neither persists via ENV, so they never leak into the final
# image config and are never confused with the real runtime values, which
# come from Railway's environment variables / .env at container start.
RUN SECRET_KEY="build-time-placeholder-unused-at-runtime" \
    FRONTEND_URL="http://build-time-placeholder" \
    python manage.py collectstatic --noinput

USER django

# EXPOSE is informational only — the real bind port is dynamic via $PORT,
# set by Railway at runtime. Docker/Compose ignore this for actual routing.
EXPOSE 8000

# Railway uses its own platform-level healthcheck (Settings > Healthcheck Path)
# against whatever port it assigns, so this HEALTHCHECK mainly matters for
# local `docker compose` runs. curl resolves the same dynamic $PORT gunicorn
# binds to below, so the two never drift out of sync with each other.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD sh -c 'curl -f "http://localhost:${PORT:-8000}/health/" || exit 1'

ENTRYPOINT ["/usr/bin/tini", "--", "/app/scripts/entrypoint.sh"]

# Bind to Railway's assigned $PORT if present, falling back to 8000 for local
# Compose runs. Single worker + threads is safe for either Postgres or SQLite
# at low traffic; bump --workers if traffic grows and you're on Postgres.
CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 4 --worker-class gthread"]
