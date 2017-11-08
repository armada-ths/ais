from django.contrib.auth.models import User
from events.models import EventAttendence, Event
from fair.models import Fair
from django.utils import timezone

fair = Fair.objects.filter(current=True).get()
now = timezone.now()
tomorrow = now + timezone.timedelta(days=1)
yesterday = now + timezone.timedelta(days=-1)

events = Event.objects.filter(name='TestEvent')
EventAttendence.objects.filter(event__in=events).delete()
for i in range(0, events[0].capacity):
    try:
        user = User.objects.get(username=('testuser' + str(i)), email='ell.westerberg@gmail.com', first_name=('Test'+ str(i)), last_name=('User'+ str(i)))
        user.delete()
    except:
        pass
events.delete()
