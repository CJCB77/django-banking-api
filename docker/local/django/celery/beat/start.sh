#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

echo "🚀 Starting Celery Beat (migrations handled by API service)..."

# Removes any stale PID file that might prevent Beat from starting 
# (Beat writes this to track its running process).
rm -f './celerybeat.pid'

exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app beat -l INFO'