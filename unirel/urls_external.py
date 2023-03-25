from django.conf.urls import url

from unirel import views

urlpatterns = [
    url(
        r"^(?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
        views.register,
        name="unirel_register",
    )
]
