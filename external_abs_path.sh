#! /bin/sh

# return the absolute path of the relative path
# of $1.
echo "$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
