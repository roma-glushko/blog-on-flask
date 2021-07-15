#!/bin/ash

flask db upgrade
gunicorn blog:app -w 2 -b :8000 --reload