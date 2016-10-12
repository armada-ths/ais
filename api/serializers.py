from collections import OrderedDict
from lib.util import unix_time


MISSING_IMAGE = '/static/missing.png'


def absolute_url(request, path):
    protocol = 'http://' if request.is_secure else 'https://'
    url = request.META['HTTP_HOST']
    return '{}{}{}'.format(protocol, url, path)


def image_url_or_missing(request, image):
    if image:
        return absolute_url(request, image.url)
    else:
        return absolute_url(request, MISSING_IMAGE)


def company(company):
    return OrderedDict([
        ('id', company.pk),
        ('name', company.name),
    ])


def event(event):
    return OrderedDict([
        ('id', event.pk),
        ('name', event.name),
        ('image', image_url_or_missing(event.image)),
        ('description_short', event.description_short),
        ('description', event.description),
        ('event_start', unix_time(event.event_start)),
        ('event_end', unix_time(event.event_end)),
        ('registration_start', unix_time(event.registration_start)),
        ('registration_end', unix_time(event.registration_end)),
        ('registration_last_day_cancel',
            unix_time(event.registration_last_day_cancel)),
        ('tags', []),
    ])


def newsarticle(newsarticle):
    return OrderedDict([
        ('id', newsarticle.pk),
        ('title', newsarticle.title),
    ])


def partner(partner, request):
    return OrderedDict([
        ('id', partner.pk),
        ('name', partner.name),
        ('logo_url', absolute_url(request, partner.logo.url)),
        ('link_url', partner.url),
        ('is_main_partner', partner.main_partner)
    ])
