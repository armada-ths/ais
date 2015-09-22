#!/bin/sh
/bin/bash -c ". /home/eric/ais_venv/bin/activate; 
python /home/eric/ais/manage.py makemigrations --settings local_settings;
echo making migrations...;
python /home/eric/ais/manage.py migrate --settings local_settings;
echo migrating...;
python /home/eric/ais/manage.py runserver 127.0.0.1:8080 --settings local_settings"
