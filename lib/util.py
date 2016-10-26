from django.utils import timezone
import time


def has_common_element(list1, list2):
    return True if set(list1) & set(list2) else False


def before(time):
    now = timezone.now()
    return now < time


def after(time):
    now = timezone.now()
    return time < now


def unix_time(datetime):
    return int(time.mktime(datetime.timetuple()))
