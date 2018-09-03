#!/bin/bash
cd /vagrant
/vagrant/ais_venv/bin/python manage.py dbshell --settings local_settings
