#!/bin/bash
until `curl --output /dev/null --silent --head --fail http://web:8000`; do \
    echo "Waiting for web:8000. This might take a while..."; \
    sleep 5; \
done
