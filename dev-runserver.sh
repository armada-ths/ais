#!/bin/bash
cd /vagrant
/vagrant/ais_venv/bin/python manage.py runserver 0.0.0.0:8080 --settings local_settings
