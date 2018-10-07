from django.conf.urls import url

from banquet.views import ExternalInviteView

urlpatterns = [
	url(r'^invitation/(?P<token>[0-9A-Fa-f-]+)/$', ExternalInviteView.as_view(), name = 'external_invite'),
]
