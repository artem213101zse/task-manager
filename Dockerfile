# ==========================================
# Multi-stage Dockerfile for Django (2026 best practices)
# Builder stage for wheels → slim final image + non-root user
# ==========================================

# ---- Builder ----
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for building psycopg2 etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ---- Final runtime ----
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Runtime deps only (no gcc)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Pre-create volume mount points (prevents permission issues with named volumes)
RUN mkdir -p /app/staticfiles /app/media && chown -R appuser:appuser /app

# Install wheels
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /wheels/*

# Copy project (chown for appuser)
COPY --chown=appuser:appuser . /app

# Entrypoint
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//g' /app/entrypoint.sh && chmod +x /app/entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "task_manager.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--worker-class", "gthread", "--pid", "/tmp/gunicorn.pid", "--access-logfile", "-", "--error-logfile", "-"]
