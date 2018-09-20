from django.conf.urls import url
from banquet.views import InternalInviteView, ExternalInviteView

from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
	url(r'^internal_invite/$', InternalInviteView.as_view(), name = 'internal_invite'),
	url(r'^invite/$', ExternalInviteView.as_view(), name = 'external_invite'),
]
