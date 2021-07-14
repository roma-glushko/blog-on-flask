#!/bin/ash

docker-compose -f docker-compose.production.yaml build
docker-compose -f docker-compose.production.yaml up -d