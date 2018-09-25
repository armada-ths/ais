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
silent sudo apt-get install -y libpq-dev python3-pip postgresql postgresql-contrib nodejs npm
silent sudo pip3 install virtualenv
silent virtualenv ais_venv
silent source ais_venv/bin/activate
silent pip3 install -r requirements.txt

echo "Setting up database..."

# We would like to be able to access the database without having to sign in
silent sudo sed -i 's/peer/trust/' /etc/postgresql/*/main/pg_hba.conf
silent sudo sed -i 's/md5/trust/' /etc/postgresql/*/main/pg_hba.conf
silent sudo service postgresql reload

echo "CREATE USER ais_dev PASSWORD 'ais_dev';" | silent sudo -u postgres psql
# Allow ais_dev to create databases in order to create test databases
echo "ALTER USER ais_dev CREATEDB;" | silent sudo -u postgres psql
silent sudo -u postgres createdb ais_dev
echo "GRANT ALL PRIVILEGES ON DATABASE ais_dev TO ais_dev;" | silent sudo -u postgres psql

echo "Configuring..."
silent python manage.py migrate --settings local_settings
silent python manage.py makemigrations --settings local_settings
silent python manage.py migrate --settings local_settings

echo "Sprinkling magic..."
echo "cd /vagrant" >> ~/.bashrc
echo "export DJANGO_SETTINGS_MODULE=ais.local.settings" >> ~/.bashrc
echo "source ais_venv/bin/activate" >> ~/.bashrc

echo "All done, good job everybody!"
rm -f $logfile

