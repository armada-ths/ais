## Getting Started Windows
[Installing python 3](https://www.python.org/downloads/), be sure to add python to PATH. If doing a custom install: also install pip (and tcl for virtualenv).

Navigate to a folder which you want to work in.

(Optional) Set up the virtual environment:
```
pip install virtualenv
virtualenv env
```
virtualenv supports both cmd and powershell. Activate it with activate.bat or activate.ps1, respectively.
```
env\Scripts\activate.bat
```
```
env\Scripts\activate.ps1
```

Install dependencies, get the code, create the database, run the server:
```
pip install -r requirements_local.txt
git clone http://github.com/armada-ths/ais
python ais\manage.py migrate --settings local_settings
python ais\manage.py runserver --settings local_settings
```
To be able to log in to the local version of ais we create a superuser:
```
python ais\manage.py createsuperuser --settings local_settings
```
When a change to a model is made, the database need to be migrated to the new format. This is done with the following:
```
python ais\manage.py makemigrations --settings local_settings
python ais\manage.py migrate --settings local_settings
```

TIP: To avoid having to type `--settings local_settings` all the time, the environement variable `DJANGO_SETTINGS_MODULE` can be set to local_settings which will tell django to use the "local_settings.py" as default.

In powershell:
```
[Environment]::SetEnvironmentVariable("DJANGO_SETTINGS_MODULE", "local_settings", "User")
```

Or do it manually in System properties.

Deactivating virtualenv is done with `deactivate`.
