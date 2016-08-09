#!/bin/sh
/bin/bash -c ". ../ais_venv/bin/activate; 
pip3 install -r requirements.txt
python3 manage.py makemigrations --settings local_settings;
echo making migrations...;
python3 manage.py migrate --settings local_settings;
echo migrating...;
python3 manage.py runserver 127.0.0.1:9005 --settings local_settings"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell --settings local_settings