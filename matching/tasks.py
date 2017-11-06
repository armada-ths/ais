from __future__ import absolute_import, unicode_literals
import string
import random
from fair.models import Fair
from banquet.models import BanquetteAttendant


from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

#from celery import shared_task
from celery.decorators import task

from .algorithms import main_classify as classify

@task(name="classify_student")
def classify_student(student_pk, survey_pk, num_of_results):
    classify.classify(student_pk, survey_pk, num_of_results)
    return 'Student got classified!'

@task(name="random_user_creation")
def create_random_user():
    first_name = 'testbanquet_{}'.format(get_random_string(10, string.ascii_letters))
    email = '{}@hotmail.com'.format(first_name)
    last_name = get_random_string(50)
    BanquetteAttendant.objects.create(first_name=first_name, last_name=last_name, email=email, fair=Fair.objects.get(current=True), gender="male", phone_number="00000")
    return 'RANDOM BANQUETTE ATTND CREATED!'
