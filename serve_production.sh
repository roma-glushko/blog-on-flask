#!/bin/ash

flask db upgrade
gunicorn blog:app -w 2 --threads 2 -b 0.0.0.0:8000