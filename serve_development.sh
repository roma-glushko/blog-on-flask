#!/bin/ash

flask db init
gunicorn blog:app -w 2 -b :8000 --reload