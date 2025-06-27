ARG PYTHON_IMAGE=python:3.10.12-slim-bullseye

# builder stage
FROM ${PYTHON_IMAGE} as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY antimpt/ antimpt/
COPY requirements.txt pyproject.toml setup.py ./

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /opt/venv/bin/pip install . --no-deps

# final stage
FROM ${PYTHON_IMAGE}

WORKDIR /antimpt

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY antimpt/ antimpt/
COPY demo/ demo/
COPY config/ config/

# execution
RUN useradd -m viewer && \
    chown -R viewer:viewer /antimpt

USER viewer

EXPOSE 8000

CMD ["python", "demo/manage.py", "runserver", "--insecure", "0.0.0.0:8000"]
