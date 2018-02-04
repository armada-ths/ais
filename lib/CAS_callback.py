from django.contrib.auth.models import User
from people.models import Profile
from lib.KTH_Catalog import lookup_user
import logging
from django.http import HttpResponseRedirect

def callback(tree):
    kth_id = tree[0][0].text
    logging.info("KTH-ID: %s trying to login" %kth_id)
    user, user_created = User.objects.get_or_create(username=kth_id)
    person = Profile(user=user)
    person.save()
