from django.utils import timezone
import calendar


def image_preview(name):
    def f(self, instance):
        return '<img src="%s" />' % getattr(instance, name).url

    f.allow_tags = True
    f.short_description = "Preview of %s" % name
    return f


def has_common_element(list1, list2):
    return True if set(list1) & set(list2) else False


def before(time):
    now = timezone.now()
    return now < time


def after(time):
    now = timezone.now()
    return time < now


def unix_time(datetime):
    return int(calendar.timegm(datetime.timetuple()))
