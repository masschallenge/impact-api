#!/usr/bin/env python3

# Figures out the next release tag given a version based on existing
# GitHub tags.
# E.g., release.py 1.2.3 => release-1.2.3.0

import sys
from urllib.request import urlopen
import json

PREFIX = "release-"


def release_tags():
    link = "https://api.github.com/repos/masschallenge/impact-api/releases"
    raw_result = urlopen(link).read()
    releases = json.loads(raw_result.decode("utf-8"))
    return [release["tag_name"] for release in releases]


def next_release(version, tags):
    full_prefix = "{prefix}{version}".format(prefix=PREFIX, version=version)
    suffixes = [tag.split(".")[-1]
                for tag in tags if tag.startswith(full_prefix)]
    numerics = [int(suffix) for suffix in suffixes if suffix.isdigit()]
    numerics.append(-1)
    maximum = max(numerics)
    return "{prefix}.{release}".format(prefix=full_prefix, release=maximum + 1)


tags = release_tags()
version = None
if len(sys.argv) > 1:
    print(next_release(sys.argv[1], release_tags()))
else:
    print("Versions argument expected.  Existing release tags are:")
    tags = release_tags()
    for tag in tags:
        if tag.startswith(PREFIX):
            print(tag)
