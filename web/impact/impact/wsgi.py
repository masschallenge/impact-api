# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'impact.settings')
# environ must be set before importing jazzband/django-configurations
from configurations.wsgi import get_wsgi_application  # noqa: E402


application = get_wsgi_application()
