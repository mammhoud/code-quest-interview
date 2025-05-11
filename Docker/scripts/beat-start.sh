#! /usr/bin/env sh
# exit on error
set -o errexit
set -e


echo "--> Celery beats process"

hatch run docker:celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
