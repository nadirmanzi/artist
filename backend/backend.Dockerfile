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
    DJANGO_SETTINGS_MODULE=config.settings
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd \
    tini \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

RUN addgroup --system --gid 1000 django && \
    adduser --system --uid 1000 --group django

RUN mkdir -p /app/staticfiles /app/media/catalog /app/logs && \
    chown -R django:django /app

COPY --chown=django:django . .
COPY --chown=django:django scripts/entrypoint.sh ./scripts/
RUN chmod +x ./scripts/entrypoint.sh

# --- Build-time static collection ---
# SECRET_KEY here is a throwaway string scoped to this single RUN layer only —
# it's needed purely so settings.py imports cleanly during collectstatic.
# It is NOT written to ENV, so it does not persist in the final image config
# and is never confused with the real SECRET_KEY, which comes from .env at
# container runtime via --env-file / compose env_file.
RUN SECRET_KEY="build-time-placeholder-unused-at-runtime" \
    python manage.py collectstatic --noinput

USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health/').status==200 else 1)" || exit 1

ENTRYPOINT ["/usr/bin/tini", "--", "/app/scripts/entrypoint.sh"]

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
