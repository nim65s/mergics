#!/bin/sh

while ! nc -z postgres 5432; do sleep 1; done

if [ "$1" = gunicorn ]
then
    ./manage.py migrate
    ./manage.py collectstatic --no-input
    gunicorn --bind 0.0.0.0 testproject.wsgi
elif [ "$1" = test ]
then
    ./manage.py test
fi
