## Getting Started OSX
[Installing python 3](https://www.python.org/downloads/) ?

`brew install python3` ?

`brew install python3-pip` ?

Navigate to a folder which you want to work in.

(Optional) Set up the virtual environment:
```
pip3 install virtualenv
virtualenv -p python3 env
```
Activate it with: ?
```
source env/bin/activate
```

Install dependencies, get the code, create the database, run the server:
```
pip3 install -r requirements_local.txt
git clone http://github.com/armada-ths/ais
python3 ais/manage.py migrate --settings local_settings
python3 ais/manage.py runserver --settings local_settings
```
To be able to log in to the local version of ais we create a superuser:
```
python ais/manage.py createsuperuser --settings local_settings
```
When a change to a model is made, the database need to be migrated to the new format. This is done with the following:
```
python ais/manage.py makemigrations --settings local_settings
python ais/manage.py migrate --settings local_settings
```

TIP: To avoid having to type `--settings local_settings` all the time, the environement variable `DJANGO_SETTINGS_MODULE` can be set to local_settings which will tell django to use the "local_settings.py" as default.

In terminal: ?
```
export DJANGO_SETTINGS_MODULE=local_settings
```

Deactivating virtualenv is done with `deactivate`.
