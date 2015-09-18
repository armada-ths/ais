# django/ais
<pre>
How to setup a local dev server:
* All settings files assume that the user is named "deployment" and that we use that home folder.
* apt-get update
* apt-get -y install sudo wget git python gcc python3-dev nginx libpcre3 libpcre3-dev libpq-dev vim

* git clone -b master git@github.com:armada-ths/ais.git
* Install pip with "wget https://bootstrap.pypa.io/get-pip.py" and "python3 get-pip.py"
* Install virtualenv with pip: "sudo pip install virtualenv" (might use pip3 for python3)
* Make a virtualenv by running: "virtualenv ais_venv"
* Activate the virtualenv with ". ais_venv/bin/activate" (source can be used instead of . )

Folder structure should now be:
d+-ais_venv
d+-ais
  |->ais
  |->files/dirs etc
  
* Install pip requirements with pip install -r requirements.txt
* Run the server with "python manage.py runserver [your localip]:80 --settings local_settings
  Where local_settings.py is your local settings file (notice the lack of .py in local_settings)
  in your local_settings file, you can disable "from ais.secrets import *" and just 
  hardcode all your variables
* You dont have to install nginx and postgre on a local machine, just use runserver and sqlite3

## IF ANY PART WAS UNCLEAR, ASK AND THEN AMEND THE DOCUMENTATION ##

System req:
GCC
python3-dev
git
nginx
libpcre3 # For pcre options when running uwsgi
libpcre3-dev # For pcre options when running uwsgi
libldap2-dev # For LDAP lookups
libsasl2-dev # Also for LDAP

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


Virtualenv req:
See "requirements.txt"

*Change addr/ip, paths in _nginx.conf
*Change paths in _uwsgi.ini
*add user to www-data group

Commands:
uwsgi --ini ais_uwsgi.ini
sudo /etc/init.d/nginx start/stop/restart
sudo tail -n 10 /var/log/nginx/error.log
sudo adduser username www-data
sudo ln -s ~/deployment/ais/ais_nginx.conf /etc/nginx/sites-enabled/

Setup postgresql:
sudo apt-get install postgresql
sudo apt-get install libpq-dev
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


Other changes:
If you dont have a local postgresql server, copy the settings file to "local_settings.py" and delete lines " from ais.secrets import *" and replace 
the database entry with:
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
You can then run for example:
python manage.py shell --settings local_settings
</pre>
