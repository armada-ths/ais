# django_newen
<pre>
System req:
GCC
python-dev
git
nginx
libpcre3 # For pcre options when running uwsgi
libpcre3-dev # For pcre options when running uwsgi

# For mysql database
mysql-server
libmysqlclient-dev

# For postgre database
postgresql
libpq-dev

System recommended:
Vim
 
Global req:
virtualenv
uwsgi # For connecting django to webserver (nginx)

Virtualenv req:
django

*Change addr/ip, paths in _nginx.conf
*Change paths in _uwsgi.ini
*add user to www-data group

Commands:
uwsgi --ini HelloWorld_uwsgi.ini
sudo /etc/init.d/nginx start/stop/restart
sudo tail -n 10 /var/log/nginx/error.log
sudo adduser username www-data
sudo ln -s ~/django/HelloWorld/helloworld_nginx.conf /etc/nginx/sites-enabled/

Setup postgresql:
sudo apt-get install postgresql
sudo apt-get install libpq-dev
. newen_venv/bin/active
pip install psycopg2

vim /etc/postgresql/[version]/main/pg_hba.conf
local all all trust
host all all 127.0.0.1/32 trust


How to setup a local dev server:
* Install as pre above
* git clone -b newen git@github.com:armada-ths/newen.git
* Rename newen/ to ais/
* . ais_venv/bin/activate
* folder structure should be:
d+-ais_venv
d+-ais
  |->ais
  |->files/dirs etc

In ais/ais_nginx.conf change:
* Line 4 to correct local dirs
* Line 36 to local public IP
* Line 62, 66 and 75 to correct local dirs

In ais/ais_uwsgi.ini change:
* Line 6, 12, 23, 29 and 33  to correct local dirs

In ais/restart_uwsgi_server.sh change:
* Line 5 to correct local dir

Other changes:
If you dont have a local postgresql server, delete lines " from secrets import *" and replace 
the database entry with:
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

</pre>
