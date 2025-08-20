#!/bin/bash

set -o errexit
set -o nounset


# Like nodemon but for Python:
# Watches .py files and automatically restarts the worker 
# when code changes (great for local dev).
exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker -l INFO'