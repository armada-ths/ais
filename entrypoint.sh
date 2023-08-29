#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput
python manage.py migrate
# python manage.py flush --no-input --settings=local_settings
python manage.py runserver 0.0.0.0:3000 # AWS PORT

exec "$@"

