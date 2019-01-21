#!/bin/bash
until `curl --output /dev/null --silent --head --fail http://web:8000`; do
    echo "Waiting for web:8000. This might take a while..."
    sleep 5
done
echo "WEB BUILD COMPLETE - visit http://localhost:8000 in a browser"

until `curl --output /dev/null --silent --head --fail http://mentor_directory:1234`; do
    echo "BUILDING FRONTEND..."
    sleep 5
done
echo "FRONTEND BUILD COMPLETE - visit http://localhost:1234 in a browser"
