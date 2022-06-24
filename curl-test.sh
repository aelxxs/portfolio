#!/bin/bash

echo "Testing API Enpoints..."

echo "GET /api/timeline_post"
curl http://localhost:5000/api/timeline_post

echo "POST /api/timeline_post"

id1=$(curl -X POST http://localhost:5000/api/timeline_post -d 'name=&email=&content=') | jq ".id"
id2=$(curl -X POST http://localhost:5000/api/timeline_post -d 'name=&email=&content=') | jq ".id"
id3=$(curl -X POST http://localhost:5000/api/timeline_post -d 'name=&email=&content=') | jq ".id"

echo "DELETE /api/timeline_post"
curl -X DELETE http://localhost:5000/api/timeline_post -d 'id=$id1'
curl -X DELETE http://localhost:5000/api/timeline_post -d 'id=$id2'
curl -X DELETE http://localhost:5000/api/timeline_post -d 'id=$id3'

echo "Test Successful 🚀"