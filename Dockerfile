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

# Copy alembic files.
WORKDIR /ceae/alembic
COPY ./alembic .
WORKDIR /ceae
COPY alembic.ini .

WORKDIR /ceae/ceae
COPY ./ceae .

WORKDIR /ceae

# Avoid running the container as `root`.
USER ceae

CMD ["bash"]
