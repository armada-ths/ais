apt-get update
apt-get install -y libpq-dev
apt-get install -y python3-pip

pip3 install virtualenv

cd /vagrant
virtualenv ais_venv
source ais_venv/bin/activate
pip3 install -r requirements.txt

python manage.py makemigrations --settings local_settings
python manage.py migrate --settings local_settings

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell --settings local_settings 

