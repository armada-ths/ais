## Getting Started Ubuntu
Python 3 should be installed on ubuntu by default, however depending on the version pip3 might not be installed `sudo apt-get install python3-pip`.

Navigate to a folder which you want to work in.

(Optional) Set up the virtual environment:
```
pip3 install virtualenv
virtualenv -p python3 env
```
Activate it with:
```
source env/bin/activate
```

Install django, get the code, create the database, run the server:
```
pip3 install django
git clone http://github.com/armada-ths/ais
python3 ais/manage.py migrate --settings local_settings
python3 ais/manage.py runserver --settings local_settings
```
Now you are good to go, but if you are going to make changes to the database models some further steps need to be taken.

To use the django admin facilites (localhost:8000/admin) you need to create a django admin user:
```
python3 ais/manage.py createsuperuser --settings local_settings
```
When a change to a model is made, the database need to be migrated to the new format. This is done with the following:
```
python3 ais/manage.py makemigrations --settings local_settings
python3 ais/manage.py migrate --settings local_settings
```

TIP: To avoid having to type `--settings local_settings` all the time, the environement variable `DJANGO_SETTINGS_MODULE` can be set to local_settings which will tell django to use the "local_settings.py" as default.

In bash:
```
export DJANGO_SETTINGS_MODULE=local_settings
```
You can also put it in your bashrc to avoid having to type it each session.

Deactivating virtualenv is done with `deactivate`.
