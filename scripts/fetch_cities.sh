#!/bin/sh

set -a
source config/.env
set a+

# TODO add this as script argument
#poetry run python ceae/pipeline.py
poetry run python ceae/s3_pipeline.py