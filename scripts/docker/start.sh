#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](server | worker | beat | flower)"
    exit 1
fi

PROCESS_TYPE=$1
MODE=${2:-production}

if [ "$PROCESS_TYPE" = "server" ]; then
    # Idempotent Django commands
    python manage.py collectstatic --noinput
    # Default superuser creation
    python manage.py initadmin

    if [ "$MODE" = "debug" ]; then
        python \
            manage.py \
            runserver \
            0.0.0.0:8000
    else
        gunicorn \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --threads 4 \
            --worker-class gthread \
            --worker-tmp-dir /dev/shm \
            --access-logfile "-" \
            --error-logfile "-" \
            contestsuite.wsgi:application
    fi
elif [ "$PROCESS_TYPE" = "worker" ]; then
    if [ "$MODE" = "debug" ]; then
    celery \
        -A contestsuite \
        worker \
            --autoscale=10,1 \
            -n worker@%n \
            --loglevel DEBUG
    else
        celery \
        -A contestsuite \
        worker \
            --autoscale=10,3 \
            -n worker@pcs_django \
            --loglevel INFO
    fi
elif [ "$PROCESS_TYPE" = "beat" ]; then
    if [ "$MODE" = "debug" ]; then
        celery \
            -A contestsuite \
            beat \
                --loglevel DEBUG \
                --scheduler django_celery_beat.schedulers:DatabaseScheduler
    else
        celery \
            -A contestsuite \
            beat \
                --loglevel INFO \
                --scheduler django_celery_beat.schedulers:DatabaseScheduler
    fi
elif [ "$PROCESS_TYPE" = "flower" ]; then
    if [ "$MODE" = "debug" ]; then
        celery \
            -A contestsuite \
            flower \
                --loglevel DEBUG \
                --conf=contestsuite/flowerconfig.py
    else
        celery \
            -A contestsuite \
            flower \
                --loglevel INFO \
                --conf=contestsuite/flowerconfig.py
    fi
else
    echo "Invalid [PROCESS_TYPE](server | worker | beat | flower)"
    exit 1
fi
