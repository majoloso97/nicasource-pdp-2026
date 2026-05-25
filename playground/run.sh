#!/bin/bash

BACKEND_SRC="/app"

case $1 in
    -d|django)
        cd "$BACKEND_SRC" || exit 1
        uvicorn config.asgi:application --port 8000 --host 0.0.0.0 --reload
        ;;
    -sm|showmigrations)
        MODULE_NAME=$2
        if [ -z "$2" ]; then
            python "$BACKEND_SRC/manage.py" showmigrations
        else
            MODULE_NAME=$2
            python "$BACKEND_SRC/manage.py" showmigrations "${MODULE_NAME}"
        fi
        ;;
    -mm|makemigrations)
        MODULE_NAME=$2
        if [ -z "$2" ]; then
            python "$BACKEND_SRC/manage.py" makemigrations
        else
            MODULE_NAME=$2
            python "$BACKEND_SRC/manage.py" makemigrations "${MODULE_NAME}"
        fi
        ;;
    -mg|migrate)
        if [ -z "$2" ]; then
            python "$BACKEND_SRC/manage.py" migrate
        else
            MODULE_NAME=$2
            if [ -z "$3" ]; then
                python "$BACKEND_SRC/manage.py" migrate "${MODULE_NAME}"
            else
                MIGRATION_NUMBER=$3
                python "$BACKEND_SRC/manage.py" migrate "${MODULE_NAME}" "${MIGRATION_NUMBER}"
            fi
        fi
        ;;
    -t|test)
        if [ -z "$2" ]; then
            echo "Error: No module name provided for testing."
            echo "Usage: $0 -t <module_name>"
            exit 1
        else
            MODULE_NAME=$2
            python "$BACKEND_SRC/manage.py" test --keepdb "${MODULE_NAME}.tests"
        fi
        ;;
    -s|shell)
        python "$BACKEND_SRC/manage.py" shell
        ;;
    -m|manage)
        cd "$BACKEND_SRC" || exit 1
        python "$BACKEND_SRC/manage.py" "${@:2}"
        ;;
esac
exit
