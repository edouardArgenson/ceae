# syntax=docker/dockerfile:1

FROM python:3.9-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.13 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

RUN groupadd -r ceae && useradd --no-log-init -r -g ceae ceae

RUN apt-get update && apt-get install -y \
    curl \
    # Psycopg2 dependencies:
    gcc \
    python3-dev \
    libpq-dev \
    # Clean apt-get cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install poetry.
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && chown -R ceae:ceae /opt/poetry/
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /ceae
COPY poetry.lock pyproject.toml ./

RUN poetry check && poetry install --no-root

COPY ./db /ceae/db
RUN poetry run pip install --no-cache --no-index db/

# Copy alembic files.
COPY ./alembic /ceae/alembic
COPY alembic.ini .

COPY ./api /ceae/api

WORKDIR /ceae/api
USER ceae

CMD ["poetry", "run", "uvicorn", "main:ceae_api", "--host", "0.0.0.0", "--port", "80"]
