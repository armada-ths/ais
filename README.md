[AIS](http://ais.armada.nu/) — Armada Internal System
==================================================

Contribution Guides
--------------------------------------

In the spirit of open source software development, AIS always encourages community code contribution. To help you get started and before you jump into writing code, be sure to read these important contribution guidelines thoroughly:

1. Nothing to see here, continue to next section.
2. Actually yes there is, work on branches and send a PR for anything non-trivial. No long-running branches.

Development setup
-------------
1. Download [VirtualBox](https://www.virtualbox.org) and [Vagrant](https://www.vagrantup.com/downloads.html)
3. Clone the repo and run `vagrant up` from the repo's root
4. ☕️
5. Browse to [localhost:8080/admin](http://localhost:8080/admin) and log in with username "admin" and password "admin"
6. Browse to [localhost:8080/](http://localhost:8080/). Bam! That's your local AIS environment.

This will set up a dev environment in a virtual machine for you and port-forward the Django server so you can access it from your host operating system. The repo folder is shared with the VM and the AIS app will reload whenever files change. Basically: Write code, refresh your browser tab, repeat.

If you need ssh access to the VM just run `vagrant ssh` from the repo's root. The repo is mirrored in the `/vagrant` folder of the VM. The [Vagrant documentation](https://www.vagrantup.com/docs/) is really nice if you want to do something fancy.

# Setting up a new production server
This instructions are used for settings up a new instance of AIS

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


