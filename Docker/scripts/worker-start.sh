#! /bin/sh
# exit on error
set -o errexit
set -e
echo "--> Celery worker process"


# hatch run python /scripts/celeryworker_pre_start.py
# hatch run celery -A app.worker worker -l info -Q main-queue -c 1
# hatch run celery -A core.utils.tasks worker -l info --without-gossip --without-mingle --without-heartbeat

hatch run docker:celery -A core worker -l info --without-gossip --without-mingle --without-heartbeat
