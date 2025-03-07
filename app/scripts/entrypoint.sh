#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socket acd_app.sock --module acd_app.wsgi --chmod-socket=666