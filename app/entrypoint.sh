#!/bin/sh

if [ "$APP_ENV" = "development" ]; then
    exec python app.py
else
    exec gunicorn app:server \
    --workers 4 \
    --bind 0.0.0.0:8050 \
    --timeout 120
fi