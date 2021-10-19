#!/bin/bash
cd /vagrant
npm run build &&
npm run watch &
sudo /vagrant/ais_venv/bin/python manage.py runserver 0.0.0.0:8080 --settings local_settings
