#!/bin/bash
cd /vagrant
/vagrant/ais_venv/bin/python manage.py migrate --settings local_settings
