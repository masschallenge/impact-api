#!/bin/bash
cd /wwwroot
if [ "${DJANGO_CONFIGURATION}" == "Dev" ]
then
echo "waiting on mysql"
while ! mysqladmin ping -h"mysql" -u --silent 2>/dev/null; do
        sleep 3
        echo "..."
done
fi

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
service nginx restart
supervisord -c supervisord.conf
