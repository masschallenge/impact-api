#!/usr/bin/env python3

# Figures out the next release tag given a version based on existing
# GitHub tags.
# E.g., release.py 1.2.3 => release-1.2.3.0
# Typically run as release.py `cat VERSION`

import sys
from urllib.request import urlopen
import json

PREFIX = "release-"


def release_tags():
    link = "https://api.github.com/repos/masschallenge/impact-api/releases"
    raw_result = urlopen(link).read()
    tags = [release["tag_name"]
            for release in json.loads(raw_result.decode("utf-8"))]
    return [tag for tag in tags if tag.startswith(PREFIX)]


def next_release(version, tags):
    full_prefix = "{prefix}{version}".format(prefix=PREFIX, version=version)
    suffixes = [tag.split(".")[-1] for tag in tags]
    numerics = [int(suffix) for suffix in suffixes if suffix.isdigit()]
    numerics.append(-1)
    maximum = max(numerics)
    return "{prefix}.{release}".format(prefix=full_prefix, release=maximum + 1)


def print_release_tags(tags):
    tags = release_tags()
    if tags:
        for tag in tags:
            print(tag)
    else:
        print("No existing release tags.")


def print_tags(tags):
    if tags:
        print("Existing release tags:")
        for tag in tags:
            print(tag)
    else:
        print("No releases found.")


tags = release_tags()
version = None
if len(sys.argv) > 1:
    print(next_release(sys.argv[1], tags))
else:
    print("Version argument expected.")
    print_tags(tags)
