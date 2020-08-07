#!/bin/sh

python queue_server.py &
gunicorn -w 1 -b 0.0.0.0:8080 run_web_server:app
