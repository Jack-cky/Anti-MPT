FROM python:3.12.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore \
    DJANGO_ENV=production \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

COPY antimpt ./antimpt
COPY apps ./apps
COPY config/config.yaml ./config/config.yaml
COPY pyproject.toml ./

FROM base AS dashboard

RUN pip install --no-cache-dir --no-compile ".[dashboard]" && \
    useradd --create-home antimpt && \
    chown -R antimpt:antimpt /app

USER antimpt

EXPOSE 8000

CMD ["gunicorn", "--chdir", "apps", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--worker-class", "gthread", "--threads", "2", "--workers", "1", "--timeout", "120", "--graceful-timeout", "30", "--keep-alive", "5"]

FROM base AS pipeline

ENV PYTHONPATH=/app/apps

RUN pip install \
    torch==2.12.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu \
    --extra-index-url https://pypi.org/simple && \
    pip install --no-cache-dir --no-compile ".[pipeline]" && \
    useradd --create-home antimpt && \
    chown -R antimpt:antimpt /app

USER antimpt

CMD ["python", "-m", "apps.manage", "run_pipeline"]
