[AIS](http://ais.armada.nu/) — (THS) Armada Internal System
==================================================

Contribution Guides
--------------------------------------

In the spirit of open source software development, AIS always encourages community code contribution. To help you get started and before you jump into writing code, be sure to read these important contribution guidelines thoroughly:

1. Nothing to see here, continue to next section.

Prerequisites
-------------

- Linux system
- Installing the required applications:
```bash
apt-get update
```
```bash
apt-get -y install sudo wget git python gcc python3-dev nginx libpcre3 libpcre3-dev libldap2-dev libsasl2-dev libpq-dev
```
- Download repository from git:
```bash
git clone https://github.com/armada-ths/ais.git
```
- Installing pip:
```bash
wget https://bootstrap.pypa.io/get-pip.py
```
```bash
python3 get-pip.py
```
- Installing virtualenv:
```bash
sudo pip install virtualenv (might need to use pip3 to force python3)
```
- Creating virtualenv:
```bash
virtualenv ais_venv
```
- Activate virutalenv:
```bash
. ais_venv/bin/activate
```
- Install pip requirements
```bash
pip install -r requirements.txt
```

Running the local server
------------------------
Create a local_settngs.py file (see local_settings.py.example). Remove postgresql, remove secrets, setup templates directory etc.
- Activate virutal environment
```bash
. ais_venv/bin/activate
```
- Run server
```bash
python manage.py runserver [your local ip]:[port] --settings local_settings
```

Local settings
--------------
If you dont have a local postgresql server, copy the settings file to "local_settings.py" and delete lines " from ais.secrets import *" and replace
the database entry with:
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
You can then run for example:
python manage.py shell --settings local_settings

To run the local server you will need to always run within the vritual environment.

# Setting up a new AIS server
This instructions are used for settings up a new instance of AIS

Installing MySQL
------------------
```bash
apt-get -y install mysql-server libmysqlclient-dev
```
Installing PostgreSQL
--------------------
```bash
apt-get -y install postgresql libpq-dev
```

Server configuration
-------------------
- Change addr/ip, paths in _nginx.conf
- Change paths in _uwsgi.ini
- add user to www-data group

Commands:
uwsgi --ini ais_uwsgi.ini
sudo /etc/init.d/nginx start/stop/restart
sudo tail -n 10 /var/log/nginx/error.log
sudo adduser username www-data
sudo ln -s ~/deployment/ais/ais_nginx.conf /etc/nginx/sites-enabled/

Setup postgresql
----------------
. ais_venv/bin/activate
vim /etc/postgresql/[version]/main/pg_hba.conf
local all all trust
host all all 127.0.0.1/32 trust

(Lines changed, no longer number accurate, the idea is the same)
In ais/ais_nginx.conf change:
* Line 4 to correct local dirs
* Line 36 to local public IP
* Line 62, 66 and 75 to correct local dirs

In ais/ais_uwsgi.ini change:
* Line 6, 12, 23, 29 and 33  to correct local dirs

In ais/restart_uwsgi_server.sh change:
* Line 5 to correct local dir

Link (sudo ln -s /home/deployment/ais/ais_nginx.conf /etc/nginx/sites-enabled/) and unlink /etc/nginx/sites-enabled/default
Add your user to the group www-data with: sudo adduser username www-data


