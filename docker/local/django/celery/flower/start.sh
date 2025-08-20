#!/bin/bash

set -o errexit
set -o nounset

# Wait for broker to be ready
sleep 5

# Starts Flower, Celery’s web-based monitoring tool.
# --basic_auth → Protects the Flower UI with a username/password from environment variables.
exec watchfiles --filter python celery.__main__.main \
    --args \
    "-A config.celery_app -b ${CELERY_BROKER_URL} flower --basic_auth=${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"