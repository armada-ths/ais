from django.contrib.auth.models import User
from events.models import EventAttendence, Event
from fair.models import Fair
from django.utils import timezone

fair = Fair.objects.filter(current=True).get()
now = timezone.now()
tomorrow = now + timezone.timedelta(days=1)
yesterday = now + timezone.timedelta(days=-1)

event = Event.objects.create(
    fair=fair, name='TestEvent',
    event_start='2017-10-20 20:00',
    event_end='2017-10-20 21:00',
    capacity=300,
    confirmation_mail_subject ='confirmation',
    confirmation_mail_body='confirmation',
    rejection_mail_subject='rejection',
    rejection_mail_body='rejection',
    registration_start = yesterday,
    registration_end = tomorrow,
    )


for i in range(0, event.capacity):
    user = User.objects.create(username=('testuser' + str(i)), email='ell.westerberg@gmail.com', first_name=('Test'+ str(i)), last_name=('User'+ str(i)))
    EventAttendence.objects.create(user=user, status='S', event=event)

    
    
    
    
