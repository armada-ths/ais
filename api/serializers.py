from collections import OrderedDict
import time

def unix_time(datetime):
    return int(time.mktime(datetime.timetuple()))

def company_serializer(company):
    return OrderedDict([
        ('id', company.pk),
        ('name', company.name),
    ])

def event_serializer(event):
    return OrderedDict([
        ('id', event.pk),
        ('name', event.name),
        ('image', event.image.url if event.image else ''),
        ('description_short', event.description_short),
        ('description', event.description),
        ('event_start', unix_time(event.event_start)),
        ('event_end', unix_time(event.event_end)),
        ('registration_start', unix_time(event.registration_start)),
        ('registration_end', unix_time(event.registration_end)),
        ('registration_last_day_cancel', unix_time(event.registration_last_day_cancel)),
        ('tags', []),
    ])

def newsarticle_serializer(newsarticle):
    return OrderedDict([
        ('id', newsarticle.pk),
        ('title', newsarticle.title),
    ])
