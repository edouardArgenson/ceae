#!/bin/sh

set -a
source config/.env
set a+

poetry run alembic upgrade head

# TODO add this as script argument
#poetry run python ceae/pipeline.py
poetry run python ceae/sql_pipeline.py