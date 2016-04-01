#!/bin/sh
/bin/bash -c ". ../ais_venv/bin/activate; 
python manage.py makemigrations --settings local_settings;
echo making migrations...;
python manage.py migrate --settings local_settings;
echo migrating...;
python manage.py runserver 127.0.0.1:9005 --settings local_settings"
