FROM python:3.12.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1 \
    DJANGO_ENV=production \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

COPY antimpt ./antimpt
COPY apps ./apps
COPY config/config.yaml ./config/config.yaml
COPY pyproject.toml ./

FROM base AS dashboard

RUN --mount=from=ghcr.io/astral-sh/uv:0.10.11,source=/uv,target=/bin/uv \
    uv pip install ".[dashboard]" && \
    useradd --create-home antimpt && \
    chown -R antimpt:antimpt /app

USER antimpt

EXPOSE 8000

CMD ["gunicorn", "--chdir", "apps", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--worker-class", "gthread", "--threads", "2", "--workers", "1", "--timeout", "120", "--graceful-timeout", "30", "--keep-alive", "5"]

FROM base AS pipeline

ENV PYTHONPATH=/app/apps

RUN --mount=from=ghcr.io/astral-sh/uv:0.10.11,source=/uv,target=/bin/uv \
    uv pip install ".[pipeline]" && \
    useradd --create-home antimpt && \
    chown -R antimpt:antimpt /app

USER antimpt

CMD ["python", "-m", "apps.manage", "run_pipeline"]
