<<<<<<< HEAD
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ais.production.settings')

app = Celery('ais')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))
=======
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ais.local.settings')

app = Celery('ais')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
>>>>>>> 188af7c6c6ec9f6e6f0dec7b2eb04e0d5ac411dc
