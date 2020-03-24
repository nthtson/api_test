#!/bin/sh
set -e

until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
    python manage.py shell -c "from accounts.models import Account; Account.objects.create_superuser('$DEFAULT_SUPPORT_EMAIL', '$DEFAULT_SUPPORT_PASSWORD')"
fi

exec "$@"
