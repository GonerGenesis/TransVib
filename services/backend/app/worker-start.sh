#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

watchmedo auto-restart --directory=./app/calc/ --pattern=*.py --recursive -- celery -A app.worker worker -l info -Q main-queue -c 1
