#!/bin/ash

docker-compose -f docker-compose.development.yaml build
docker-compose -f docker-compose.development.yaml up -d