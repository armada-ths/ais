#!/bin/bash

logfile="/vagrant/provision.log"
rm -f $logfile

function silent() {
  "$@" >> $logfile 2>&1
  if [ $? -ne 0 ]; then
    echo "Oops, something bad happened!" 1>&2
    echo "See provision.log for more info." 1>&2
    exit 1
  fi
}

echo "Updating the box..."
silent sudo apt-get update

echo "Installing dependencies..."
cd /vagrant
silent sudo apt-get install -y libpq-dev python3-pip postgresql postgresql-contrib
silent sudo pip3 install virtualenv
silent virtualenv ais_venv
silent source ais_venv/bin/activate
silent pip3 install -r requirements.txt

echo "Setting up database..."
echo "create user ais password 'ais';" | silent sudo -u postgres psql
silent sudo -u postgres createdb ais
echo "grant all privileges on database ais to ais;" | silent sudo -u postgres psql
export PGPASSWORD=ais
silent psql -h 127.0.0.1 -U ais < /vagrant/scripts/vagrant/ais.sql

echo "Configuring..."
silent python manage.py migrate --settings local_settings
silent python manage.py makemigrations --settings local_settings
silent python manage.py migrate --settings local_settings
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | silent python manage.py shell --settings local_settings

echo "Sprinkling magic..."
echo "cd /vagrant" >> ~/.bashrc
echo "export DJANGO_SETTINGS_MODULE=ais.local.settings" >> ~/.bashrc
echo "source ais_venv/bin/activate" >> ~/.bashrc

echo "All done, good job everybody!"
rm -f $logfile

