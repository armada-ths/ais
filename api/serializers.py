from collections import OrderedDict
from lib.util import unix_time

MISSING_IMAGE = '/static/missing.png'
MISSING_MAP = '/static/nymble_2048.png'
MISSING_PERSON = '/static/images/no-image.png'


def tags_mappings(items):
    tags = [i.name for i in items]
    return [
        ('diversity', 'Diversity' in tags),
        ('sustainability', 'Sustainability' in tags),
        ('startup', 'Startup' in tags),
    ]


def absolute_url(request, path):
    protocol = 'https://' if request.is_secure() else 'http://'
    url = request.META['HTTP_HOST']
    return '{}{}{}'.format(protocol, url, path)


def image_url_or_missing(request, image, missing=MISSING_IMAGE):
    if image:
        return absolute_url(request, image.url)
    else:
        return absolute_url(request, missing)


def obj_name(obj):
    if not obj:
        return {}
    return OrderedDict([
        ('id', obj.pk),
        ('name', obj.name)
    ])


def names(objects):
    return [obj_name(obj) for obj in objects.all()]


def exhibitor(request, exhibitor):
    tags = tags_mappings(exhibitor.tags.all())
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
                           ('map_location_url', image_url_or_missing(request, exhibitor.location_at_fair, MISSING_MAP)),
                           ('map_url', image_url_or_missing(request, exhibitor.location_at_fair, MISSING_MAP)),
                           ('location', str(exhibitor.exhibitor.location) if exhibitor.exhibitor.location else ''),
                           ('room', str(exhibitor.exhibitor.location) if exhibitor.exhibitor.location else ''),
                           ('programs', names(exhibitor.programs)),
                           ('main_work_field', obj_name(exhibitor.main_work_field)),
                           ('work_fields', names(exhibitor.work_fields)),
                           ('job_types', names(exhibitor.job_types)),
                           ('continents', names(exhibitor.continents)),
                           ('values', names(exhibitor.values)),
                       ] + tags)


def event(request, event):
    tags = tags_mappings(event.tags.all())
    signup_link = event.external_signup_url if event.external_signup_url else absolute_url(request, '/events/' + str(
        event.pk) + '/signup')
    return OrderedDict([
                           ('id', event.pk),
                           ('name', event.name),
                           ('image_url', image_url_or_missing(request, event.image)),
                           ('location', event.location),
                           ('description_short', event.description_short),
                           ('description', event.description),
                           ('signup_link', signup_link),
                           ('event_start', unix_time(event.event_start)),
                           ('event_end', unix_time(event.event_end)),
                           ('registration_required', event.registration_required),
                           ('registration_start', unix_time(event.registration_start)),
                           ('registration_end', unix_time(event.registration_end)),
                           ('registration_last_day_cancel',
                            unix_time(event.registration_last_day_cancel)),
                       ] + tags)


def newsarticle(request, newsarticle):
    return OrderedDict([
        ('id', newsarticle.pk),
        ('title', newsarticle.title),
        ('date_published', unix_time(newsarticle.publication_date)),
        ('html_article_text', newsarticle.html_article_text),
        ('image', image_url_or_missing(request, newsarticle.image)),
    ])


def partner(request, partner):
    return OrderedDict([
        ('id', partner.pk),
        ('name', partner.name),
        ('logo_url', absolute_url(request, partner.logo.url)),
        ('link_url', partner.url),
        ('is_main_partner', partner.main_partner)
    ])


def person(request, person):
    return OrderedDict([
        ('id', person.pk),
        ('name', person.get_full_name()),
        ('picture', image_url_or_missing(request, person.profile.picture, MISSING_PERSON)),
    ])


def organization_group(request, group):
    people = [person(request, p) for p in group.user_set.all()]
    return OrderedDict([
        ('id', group.pk),
        ('role', group.name),
        ('people', people),
    ])


def banquet_placement(request, attendence, index):
    return OrderedDict([
        ('id', attendence.pk),
        ('first_name', attendence.first_name),
        ('last_name', attendence.last_name),
        ('linkedin_url', attendence.linkedin_url or ""),
        ('table', attendence.table_name or ""),
        ('seat', attendence.seat_number or ""),
        ('job_title', attendence.job_title)
    ])
