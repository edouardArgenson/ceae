#!/bin/sh

set -a
source config/.env
set a+

poetry run alembic upgrade head
poetry run python ceae/fetch_cities_weather.py