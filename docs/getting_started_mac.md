## Getting Started OSX

It is recommended that you install Python3 using `brew`. If you don't already have brew, go get it.

`brew install python3`

Navigate to a folder which you want to work in.

(Optional) Set up the virtual environment:

```bash
pip3 install virtualenv
virtualenv -p python3 venv
```
Activate it with:

```bash
source venv/bin/activate
```

Install dependencies, get the code, create the database, run the server:

```bash
pip3 install -r requirements_local.txt
git clone http://github.com/armada-ths/ais
python3 ais/manage.py migrate --settings local_settings
python3 ais/manage.py runserver --settings local_settings
```
To be able to log in to the local version of ais we create a superuser:
```bash
python3 ais/manage.py createsuperuser --settings local_settings
```
When a change to a model is made, the database need to be migrated to the new format. This is done with the following:
```bash
python3 ais/manage.py makemigrations --settings local_settings
python3 ais/manage.py migrate --settings local_settings
```

TIP: To avoid having to type `--settings local_settings` all the time, the environement variable `DJANGO_SETTINGS_MODULE` can be set to local_settings which will tell django to use the "local_settings.py" as default.

In terminal:
```bash
export DJANGO_SETTINGS_MODULE=local_settings
```

You can also put it in your .bashrc or .zshrc to avoid having to type it each session.

Deactivating virtualenv is done with `deactivate`.
