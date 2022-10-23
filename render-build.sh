#!/usr/bin/env bash
set -o errexit

poetry install --no-dev
python manage.py collectstatic --noinput
python manage.py compress --force
python manage.py collectstatic --noinput
python manage.py migrate
