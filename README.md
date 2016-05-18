[AIS](http://ais.armada.nu/) — Armada Internal System
==================================================

Contribution Guides
--------------------------------------

In the spirit of open source software development, AIS always encourages community code contribution. To help you get started and before you jump into writing code, be sure to read these important contribution guidelines thoroughly:

1. Nothing to see here, continue to next section.

Installation
-------------
Our preferred build environment is a Debian 8.3 x64 [Digital Ocean](https://www.digitalocean.com) droplet (the cheapest one will do for testing). Mileage may vary on other systems. If something doesn't work (likely) then [let us know](https://github.com/armada-ths/ais/issues/new) 🍻

### Set up the locale
First off, you're going to need to fix your locale if you're on a clean DO droplet. Add the following lines to `/etc/default/locale`:
```bash
LANG="en_US.UTF-8"
LC_ALL="en_US.UTF-8"
LANGUAGE="en_US.UTF-8"
```
and then **log out** before logging back in again. The output of the `locale` command should now look something like this:
```bash
LANG=en_US.UTF-8
LANGUAGE=en_US.UTF-8
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=en_US.UTF-8
```
### Install all the things
```bash
apt-get update
apt-get -y install sudo wget git python gcc python3-dev python3-pip nginx libpcre3 libpcre3-dev libpq-dev vim
pip3 install virtualenv
```

### Download and install the AIS code:
```bash
git clone https://github.com/armada-ths/ais.git
```
It's all downhill from here!
```bash
cd ais
virtualenv ais_venv
. ais_venv/bin/activate
pip3 install -r requirements.txt
```

Running the local server
------------------------
Create a local_settngs.py file (see local_settings.py.example) or the Local settings section.
- Make migrations
```bash
python manage.py makemigration --settings local_settings
```
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
Read this section if you do not want to use a PostgreSQL.
- Copy a the settings.py file to the /ais/ root directory or use the the local_settings.py.example file
- Install SQLite
```bash
apt-get -y install sqlite3
```
- Delete line about secrets (this file is not present in git and will NEVER be)
```bash
from ais.secrets import *
```
- Delete database lines and replace with SQLite3
```bash
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
```
- You also need to setup the directories (so it points to your local directories for static files, templates and such)

- To run the local server you will need to always run within the vritual environment.

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


