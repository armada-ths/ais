cd /vagrant
source ais_venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8080 --settings local_settings &
