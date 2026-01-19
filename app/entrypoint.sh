#!/usr/bin/env bash

if [ "$APP_ENV" = "production" ]; then
    exec gunicorn app:server \
    --workers 4 \
    --bind 0.0.0.0:8050 \
    --timeout 120
else
    exec python app.py
fi