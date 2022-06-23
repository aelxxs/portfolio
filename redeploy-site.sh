#!/bin/bash

git fetch && git reset origin/main --hard
docker compose -f ".docker\docker-compose.yaml" down
docker compose -f ".docker\docker-compose.yaml" up -d --build