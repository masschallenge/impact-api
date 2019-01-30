# MIT License
# Copyright (c) 2017 MassChallenge, Inc.

import newrelic.agent  # Must be first, per NR docs
import os
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'impact.settings')

# environ must be set before importing jazzband/django-configurations
from configurations.wsgi import get_wsgi_application  # noqa: E402

newrelic_application = newrelic.agent.wsgi_application()
application = newrelic_application(get_wsgi_application())
newrelic.agent.initialize(
    settings.NEW_RELIC_CONFIG_FILE,
    settings.NEW_RELIC_ENVIRONMENT)
