#!/bin/bash
cd /wwwroot
if [ "${DJANGO_CONFIGURATION}" == "Dev" ]; then
  echo "waiting on mysql"
  while ! mysqladmin ping -h"mysql" -u --silent 2>/dev/null; do
        sleep 3
        echo "..."
  done
fi

if [ -e "/wwwroot/static/dist/index.html" ]
then
	cp /wwwroot/static/dist/index.html templates/directory.html
fi

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput

if [ "${DJANGO_CONFIGURATION}" == "Prod" ]
then
    remote_syslog
fi

service nginx restart
supervisord -c supervisord.conf
