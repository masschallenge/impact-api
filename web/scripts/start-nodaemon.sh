#!/bin/bash
cd /wwwroot
supervisorctl stop django
python3 manage.py runserver 0.0.0.0:8000
supervisorctl start django