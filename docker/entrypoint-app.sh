#!/bin/sh
set -eu

python manage.py wait_for_db

python - <<'PY'
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
from django.db import connection
from django.core.management import call_command

django.setup()

if connection.vendor == 'postgresql':
    with connection.cursor() as cursor:
        cursor.execute('SELECT pg_advisory_lock(8855001)')

try:
    call_command('migrate', interactive=False)
    call_command('collectstatic', clear=True, interactive=False)
finally:
    if connection.vendor == 'postgresql':
        with connection.cursor() as cursor:
            cursor.execute('SELECT pg_advisory_unlock(8855001)')
PY

exec "$@"
