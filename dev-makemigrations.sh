#!/bin/bash
cd /vagrant
/vagrant/ais_venv/bin/python manage.py makemigrations --settings local_settings
