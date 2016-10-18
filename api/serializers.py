from collections import OrderedDict
from lib.util import unix_time


MISSING_IMAGE = '/static/missing.png'


def tags_mappings(items):
    tags = [i.name for i in items]
    return [
        ('diversity', 'Diversity' in tags),
        ('sustainability', 'Sustainability' in tags),
    ]


def absolute_url(request, path):
    protocol = 'http://' if request.is_secure else 'https://'
    url = request.META['HTTP_HOST']
    return '{}{}{}'.format(protocol, url, path)


def image_url_or_missing(request, image):
    if image:
        return absolute_url(request, image.url)
    else:
        return absolute_url(request, MISSING_IMAGE)


def obj_name(obj):
    return OrderedDict([
        ('id', obj.pk),
        ('name', obj.name)
        ])


def names(objects):
    return [obj_name(obj) for obj in objects.all()]


def exhibitor(request, exhibitor):
    return OrderedDict([
        ('id', exhibitor.pk),
        ('name', exhibitor.display_name),
        ('slug', exhibitor.slug),
        ('short_description', exhibitor.short_description),
        ('description', exhibitor.description),
        ('employees_sweden', exhibitor.employees_sweden),
        ('employees_world', exhibitor.employees_world),
        ('countries', exhibitor.countries),
        ('website_url', exhibitor.website_url),
        ('facebook_url', exhibitor.facebook_url),
        ('twitter_url', exhibitor.twitter_url),
        ('linkedin_url', exhibitor.linkedin_url),
        ('logo_url', image_url_or_missing(request, exhibitor.logo)),
        ('logo_small_url',
            image_url_or_missing(request, exhibitor.logo_small)),
        ('ad_url', image_url_or_missing(request, exhibitor.ad)),
        ('programs', names(exhibitor.programs)),
        ('main_work_field', obj_name(exhibitor.main_work_field)),
        ('work_fields', names(exhibitor.work_fields)),
        ('job_types', names(exhibitor.job_types)),
        ('continents', names(exhibitor.continents)),
        ('values', names(exhibitor.values)),
        *tags_mappings(exhibitor.tags.all()),
    ])


def event(request, event):
    tags = tags_mappings(event.tags.all())
    return OrderedDict([
        ('id', event.pk),
        ('name', event.name),
        ('image_url', image_url_or_missing(request, event.image)),
        ('description_short', event.description_short),
        ('description', event.description),
        ('event_start', unix_time(event.event_start)),
        ('event_end', unix_time(event.event_end)),
        ('registration_required', event.registration_required),
        ('registration_start', unix_time(event.registration_start)),
        ('registration_end', unix_time(event.registration_end)),
        ('registration_last_day_cancel',
            unix_time(event.registration_last_day_cancel)),
        *tags,
    ])


def newsarticle(newsarticle):
    return OrderedDict([
        ('id', newsarticle.pk),
        ('title', newsarticle.title),
    ])


def partner(request, partner):
    return OrderedDict([
        ('id', partner.pk),
        ('name', partner.name),
        ('logo_url', absolute_url(request, partner.logo.url)),
        ('link_url', partner.url),
        ('is_main_partner', partner.main_partner)
    ])
