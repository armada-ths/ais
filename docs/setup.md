# Setting up a server

This is the documentation for setting up development, staging and production servers for AIS.

##  Development (local) servers

### The easy way
1. Download [VirtualBox](https://www.virtualbox.org) and [Vagrant](https://www.vagrantup.com/downloads.html)
3. Clone the repo and run `vagrant up` from the repo's root
4. ☕️
5. Browse to [localhost:8080/admin](http://localhost:8080/admin) and log in with username "admin" and password "admin"
6. Browse to [localhost:8080/](http://localhost:8080/). Bam! That's your local AIS environment.

This will set up a dev environment in a virtual machine for you and port-forward the Django server so you can access it from your host operating system. The repo folder is shared with the VM and the AIS app will reload whenever files change. Basically: Write code, refresh your browser tab, repeat.

If you need ssh access to the VM just run `vagrant ssh` from the repo's root. The repo is mirrored in the `/vagrant` folder of the VM. The [Vagrant documentation](https://www.vagrantup.com/docs/) is really nice if you want to do something fancy.

### The hard way
Our preferred build environment is a Debian 8.3 x64 [Digital Ocean](https://www.digitalocean.com) droplet (the cheapest one will do for testing). Mileage may vary on other systems. If something doesn't work (likely) then [let us know](https://github.com/armada-ths/ais/issues/new) 🍻

#### Set up the locale
First off, your DO droplet will likely complain about your locale settings. To fix this you can comment out the line
```bash
SendEnv LANG LC_*
```
in your **local** machine's `ssh_config` (might be at `/etc/ssh/ssh_config`). 

#### Install all the things
```bash
apt-get update
apt-get -y install sudo wget git python gcc python3-dev python3-pip nginx libpcre3 libpcre3-dev libpq-dev vim
pip3 install virtualenv
```

#### Download and install the AIS code:
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

#### Running the local server
Create a local_settngs.py file (see local_settings.py.example) or the Local settings section.
- Make migrations
```bash
python manage.py makemigrations --settings local_settings
```
- Activate virutal environment
```bash
. ais_venv/bin/activate
```
- Run server
```bash
python manage.py runserver [your local ip]:[port] --settings local_settings
```

#### Local settings
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

## Production servers
This instructions are used for settings up a new instance of AIS

### Installing PostgreSQL
```bash
apt-get -y install postgresql libpq-dev
```

### Server configuration
- Change addr/ip, paths in _nginx.conf
- Change paths in _uwsgi.ini
- add user to www-data group

Commands:
uwsgi --ini ais_uwsgi.ini
sudo /etc/init.d/nginx start/stop/restart
sudo tail -n 10 /var/log/nginx/error.log
sudo adduser username www-data
sudo ln -s ~/deployment/ais/ais_nginx.conf /etc/nginx/sites-enabled/

### Setup postgresql
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

