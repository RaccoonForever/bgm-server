#!/bin/sh

python queue_server.py &
gunicorn -w 2 -b :8080 run_web_server:app
