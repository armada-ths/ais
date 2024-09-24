from django.conf.urls import url

from exhibitors import api

from corsheaders.signals import check_request_enabled

app_name = "exhibitors_api"


def cors_allow_api_to_exhibitors(sender, request, **kwargs):
    return request.path.startswith("/api/exhibitors")


check_request_enabled.connect(cors_allow_api_to_exhibitors)

urlpatterns = [
    url(r"^$", api.exhibitors),
    url(r"^locations$", api.locations),
    url(r"^locations/(?P<location_pk>[0-9]+)$", api.location),
    url(r"^locations/(?P<location_pk>[0-9]+)/create_booth$", api.create_booth),
    url(r"^locations/(?P<location_pk>[0-9]+)/people_count$", api.people_count),
    url(r"^days$", api.days),
    url(r"^chats/(?P<exhibitor_pk>[0-9]+)$", api.chat_messages),
    url(r"^chats/(?P<exhibitor_pk>[0-9]+)/send_message$", api.post_chat_message),
]
