#!/bin/bash
cd /code/
git diff --name-only $BRANCH | grep -v "^\.\/\.venv" | grep "__init__\.py" | xargs -r pep8 --ignore E902; git diff --name-only $BRANCH | grep "\.py" | grep -v "__init__\.py" | grep -v "^\.\/\.venv" | xargs -r flake8