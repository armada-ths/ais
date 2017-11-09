## Getting Started Ubuntu
Python 3 should be installed on ubuntu by default, and pip should already be installed but might need upgrading. You can find instructions on how to do that here:

```
https://pip.pypa.io/en/stable/installing/#upgrading-pip
```

Navigate to a folder which you want to work in.

(Optional) Set up the virtual environment:
```
pip install virtualenv
virtualenv -p python3 env
```
Activate it with:
```
source env/bin/activate
```

Install dependencies, get the code, create the database, run the server:
```
pip install -r requirements_local.txt
git clone http://github.com/armada-ths/ais
python3 ais/manage.py migrate --settings local_settings
python3 ais/manage.py runserver --settings local_settings
```

To be able to log in to the local version of ais we create a superuser:
```
python3 ais/manage.py createsuperuser --settings local_settings
```

After creating a superuser, login to AIS and create a fair from the admin view
```
http://localhost:8000/admin
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
You can also put it in your .bashrc to avoid having to type it each session.

Deactivating virtualenv is done with `deactivate`.
