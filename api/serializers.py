from collections import OrderedDict
from lib.util import unix_time
from people.models import Profile

from matching.models import StudentQuestionType as QuestionType


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
      ('first_name', host.first_name),
      ('last_name', host.last_name),
      ('email', host.email),
    ]) for host in exhibitor.hosts.all()]
    try:
      contact = OrderedDict([
        ('name', exhibitor.contact.name),
        ('email', exhibitor.contact.email),
        ('title', exhibitor.contact.title),
        ])
    except AttributeError:
      contact = None
    try:
        location = exhibitor.location.name
    except AttributeError:
        location = None
    return OrderedDict([
                           ('fair', exhibitor.fair.name),
                           ('company', company.name),
                           ('company_website', company.website),
                           ('phone_number', company.phone_number),
                           ('address_street', company.address_street),
                           ('address_zip_code', company.address_zip_code),
                           ('address_country', company.address_country),
                           ('address_city', company.address_city),
                           ('address_other_information', company.additional_address_information),
                           ('organisation_type', company.organisation_type),
                           ('company_contact', contact),
                           ('exhibitor_location', location),
                           ('booth_number', exhibitor.booth_number),
                           ('about', exhibitor.about_text),
                           ('facts', exhibitor.facts_text),
                           ('hosts', hosts),
                           ('logo_url', image_url_or_missing(request, exhibitor.logo)),
                       ])


def event(request, event):
    tags = tags_mappings(event.tags.all())
    signup_link = event.external_signup_url if event.external_signup_url else absolute_url(request, '/fairs/2017/events/' + str(
        event.pk) + '/signup')
    print(event.image)
    return OrderedDict([
                           ('id', event.pk),
                           ('name', event.name),
                           ('image_url', image_url_or_missing(request, event.image_original)),
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


def person(request, person, role):
  #Check that there are a profile for the user
    try:
      profile = person.profile
      try: 
        programme = profile.programme.name
      except AttributeError:
        programme = None
      return OrderedDict([
        ('id', profile.user.pk),
        ('name', profile.user.get_full_name()),
        ('picture', image_url_or_missing(request, profile.picture_original, MISSING_PERSON)),
        ('linkedin_url', profile.linkedin_url),
        ('programme', programme),
        ('role', role)
      ])
    except Profile.DoesNotExist: #There are no profile for this user
      return OrderedDict([
          ('id', person.pk),
          ('name', person.get_full_name()),
          ('role', role)
      ])



def organization_group(request, group):
    people = [person(request, p, group.name) for p in group.user_set.all()]
    return OrderedDict([
        ('id', group.pk),
        ('role', group.name),
        ('people', people)
    ])


def banquet_placement(request, attendence):
    try:
      table = attendence.table.name
    except AttributeError: 
      table = None
    return OrderedDict([
        ('id', attendence.pk),
        ('first_name', attendence.first_name),
        ('last_name', attendence.last_name),
        ('linkedin_url', attendence.linkedin_url or ""),
        ('table', table or ""),
        ('seat', attendence.seat_number or ""),
        ('job_title', attendence.job_title)
    ])


def serialize_slider(question):
    '''
    Serialize a SLIDER question.
    '''
    question = question.studentquestionslider
    return OrderedDict([
        ('id', question.pk),
        ('type', question.question_type),
        ('question', question.question),
        ('min', question.min_value),
        ('max', question.max_value),
        ('logarithmic', question.logarithmic),
        ('units', question.units)
    ])


def serialize_grading(question):
    '''
    Serialize a GRADING question.
    '''
    question = question.studentquestiongrading
    return OrderedDict([
        ('id', question.pk),
        ('type', question.question_type),
        ('question', question.question),
        ('count', question.grading_size)
    ])


# A dictionary of serializer functions, that avoids a huge (eventually) switch-block
QUESTION_SERIALIZERS = {
    QuestionType.SLIDER.value : serialize_slider,
    QuestionType.GRADING.value : serialize_grading
}

def question(question):
    '''
    Serialize a StudentQuestionBase child question.
    '''
    # theoretically we could have a common process for every question (the question itself and its type)
    # but that adds unncecessary complexity to the code, without optimizing or simplifying it
    if question.question_type in QUESTION_SERIALIZERS:
        return QUESTION_SERIALIZERS[question.question_type](question)
    return []   # could not serialize a type


def work_area(area):
    '''
    Serialize a work field area
    '''
    return OrderedDict([
        ('id', area.pk),
        ('field', area.work_field),
        ('area', area.work_area.work_area)
    ])
