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


Django-cas:
This module is semi-broken, to its views.py file add:
from django.contrib import messages
and remove get_host from: from django.http import
Replace get_host(request) with request.get_host()
Replace request.user.message_set.create(message=message) with messages.success(request, message)
</pre>
