from django.utils import timezone
import time


def before(time):
    now = timezone.now()
    return now < time


def after(time):
    now = timezone.now()
    return time < now


def unix_time(datetime):
    return int(time.mktime(datetime.timetuple()))
