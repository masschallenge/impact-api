#!/bin/bash
cd /wwwroot
if [ "${DJANGO_CONFIGURATION}" == "Dev" ]; then
  echo "waiting on mysql"
  while ! mysqladmin ping -h"mysql" -u --silent 2>/dev/null; do
        sleep 3
        echo "..."
  done
fi

PDT_MIGRATION_APPLIED=$(python3 manage.py showmigrations pdt | grep 0002 | grep X);
if [[ -z $PDT_MIGRATION_APPLIED ]];
then
  echo "ALTER TABLE django_content_type MODIFY COLUMN NAME VARCHAR(100) NOT NULL DEFAULT '';" | ./manage.py dbshell
  python3 manage.py migrate pdt 0002 --fake --noinput;
fi
# todo: remove this conditional after the transition is over
python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput

if [ "${DJANGO_CONFIGURATION}" == "Prod" ]
then
    remote_syslog
fi

service nginx restart
supervisord -c supervisord.conf
