from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
import logging

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

from people.models import Profile
from lib.KTH_Catalog import lookup_user, merge_user_info


oauth = OAuth()
oauth.register(
    name='kth',
    server_metadata_url='https://login.ug.kth.se/adfs/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email username',
    },
    authorization_endpoint='https://login.ug.kth.se/adfs/oauth2/authorize/',
    token_endpoint = 'https://login.ug.kth.se/adfs/oauth2/token/',
    response_type = 'code',
)

def kth_login(request):
	# redirect_uri = request.build_absolute_uri('oidc/kth/callback')
	redirect_uri = 'http://localhost:8080/oidc/kth/callback'
	return oauth.kth.authorize_redirect(request, redirect_uri)


def authorize(request):
	token = oauth.kth.authorize_access_token(request)
	user = oauth.kth.parse_id_token(request, token)
	request.session['user'] = user
	kth_id = user['kthid']

	# Steps above (2 & 3)
	callback(request, kth_id)
	print(user)
	#user = authenticate(user=request.session['user'])
	#print(user)

	return redirect('/')


def callback(request, kth_id):
	logging.info('KTH-ID: %s trying to login' %kth_id)
	
	user, user_created = User.objects.get_or_create(username = kth_id)
	user_info = lookup_user(kth_id)

	if merge_user_info(user, user_info):
		user.save()

	profile = Profile.objects.filter(user = user).first()
	if profile is None:
		Profile(user = user, no_dietary_restrictions = False).save()

	login(request, user, backend='django.contrib.auth.backends.ModelBackend')

	return HttpResponse(status=200)