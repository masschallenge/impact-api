#!/bin/bash
until `curl --output /dev/null --silent --head --fail http://web:8000`; do \
    echo "Waiting for web:8000..."; \
    sleep 5; \
done
