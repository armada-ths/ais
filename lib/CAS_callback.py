from django.contrib.auth.models import User
from people.models import Profile
from lib.KTH_Catalog import lookup_user
import logging
from django.http import HttpResponseRedirect

def callback(tree):
	kth_id = tree[0][0].text
	logging.info("KTH-ID: %s trying to login" %kth_id)
	
	user, user_created = User.objects.get_or_create(username = kth_id)
	
	ldap = lookup_user(kth_id)
	
	if ldap is not None:
		if ldap["first_name"] is not None:
			user.first_name = ldap["first_name"]
		
		if ldap["last_name"] is not None:
			user.last_name = ldap["last_name"]
		
		if ldap["email"] is not None and (user.email is None or user.email.endswidth('@kth.se')):
			user.email = ldap["email"]
		
		user.save()
	
	person, person_created = Profile.objects.get_or_create(user = user)
	person.save()
