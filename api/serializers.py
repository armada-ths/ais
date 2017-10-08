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


def exhibitor(request, exhibitor, company):
    hosts = [OrderedDict([ 
      ('first name', host.first_name),
      ('last name', host.last_name),
      ('email', host.email),
    ]) for host in exhibitor.hosts.all()]
    if exhibitor.contact:
      contact = OrderedDict([
        ('name', exhibitor.contact.name),
        ('email', exhibitor.contact.email),
        ('title', exhibitor.contact.title),
        ])
    else:
      contact = {}
    return OrderedDict([
                           ('fair', exhibitor.fair.name),
                           ('company', company.name),
                           ('company website', company.website),
                           ('phone number', company.phone_number),
                           ('address street', company.address_street),
                           ('address zip code', company.address_zip_code),
                           ('address country', company.address_country),
                           ('address city', company.address_city),
                           ('address other information', company.additional_address_information),
                           ('organisation type', company.organisation_type),
                           ('company contact', contact),
                           ('exhibitor location', exhibitor.location),
                           ('booth number', exhibitor.booth_number),
                           ('about', exhibitor.about_text),
                           ('facts', exhibitor.facts_text),
                           ('hosts', hosts),
                           ('logo url', image_url_or_missing(request, exhibitor.logo)),
                       ])


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
