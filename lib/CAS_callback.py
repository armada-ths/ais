import logging

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse

from people.models import Profile
from lib.KTH_Catalog import lookup_user, merge_user_info


def callback(tree):
	kth_id = tree[0][0].text

	logging.info('KTH-ID: %s trying to login' %kth_id)
	
	user, user_created = User.objects.get_or_create(username = kth_id)
	user_info = lookup_user(kth_id)

	if merge_user_info(user, user_info):
		user.save()

	profile = Profile.objects.filter(user = user).first()
	if profile is None:
		Profile(user = user, no_dietary_restrictions = False).save()

	return HttpResponse(status=200)