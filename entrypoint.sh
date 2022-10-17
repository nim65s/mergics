#!/bin/sh

while ! nc -z postgres 5432; do sleep 1; done

if [ "$1" = gunicorn ]
then
    poetry run ./manage.py migrate
    poetry run ./manage.py collectstatic --no-input
    poetry run gunicorn --bind 0.0.0.0 testproject.wsgi
elif [ "$1" = test ]
then
    poetry run ./manage.py test
fi
