#!/bin/bash
cd /wwwroot
if [ "${DJANGO_CONFIGURATION}" == "Dev" ]; then
  echo "waiting on mysql"
  while ! mysqladmin ping -h"mysql" -u --silent 2>/dev/null; do
        sleep 3
        echo "..."
  done
fi

if [ -e "/wwwroot/static/front-end-dist/index.html" ]
then
	cp /wwwroot/static/front-end-dist/index.html templates/front-end.html
fi

python3 manage.py collectstatic --noinput
python3 manage.py graphql_schema --schema impact.graphql.schema.schema --indent=2

if [ "${DJANGO_CONFIGURATION}" == "Prod" ]
then
    remote_syslog
fi

service nginx restart
supervisord -c supervisord.conf
