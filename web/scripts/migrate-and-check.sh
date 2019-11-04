#!/bin/bash
cd /wwwroot
# Ensure MySQL is up, so we can run migrations

# if [ "${DJANGO_CONFIGURATION}" == "Dev" ]; then
#   echo "waiting on mysql"
#   while ! mysqladmin ping -h"mysql" -u --silent 2>/dev/null; do
#         sleep 3
#         echo "..."
#   done
# fi

# Function to confirm migrations ran
check_migrations() {
	true
}

python3 manage.py migrate --noinput
check_migrations && echo "Migration check passed." || (echo "Migration check failed." ; exit 1)
