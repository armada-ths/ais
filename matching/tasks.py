import string

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

#@shared_task
#def create_random_user_accounts(total):
#    """
#    Task for testing message queue
#    """
#    for i in range(int(total)):
#        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
#        email = '{}@example.com'.format(username)
#        password = get_random_string(50)
#        User.objects.create_user(username=username, email=email, password=password)
#    return '{} random users created with success!'.format(total)

@shared_task
def create_random_user():
    """
    Another Task for testing message queue
    """
    username = 'userrrrr_{}'.format(get_random_string(10, string.ascii_letters))
    email = '{}@hotmail.com'.format(username)
    password = get_random_string(50)
    User.objects.create_user(username=username, email=email, password=password)
    return 'RANDOM USER CREATED!'
