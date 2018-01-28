from django.utils.timezone import utc
from fair.models import Fair
import datetime

def get_time_flag(close_offset = 7, warning_offset = 7):
    # used to close cr, a warning text after deadline will pop up, however exhibitors will not be permitted to do any changes after the offset in days has passed
    currentFair = None
    try:
        currentFair = Fair.objects.get(current=True)
        if currentFair.complete_registration_close_date:
            end_time = currentFair.complete_registration_close_date.replace(tzinfo=utc)
            end_time_close = end_time + datetime.timedelta(days=close_offset)
            time = datetime.datetime.now().replace(tzinfo=utc)
            time = time.replace(microsecond=0)
            warning_time = end_time - datetime.timedelta(days=warning_offset)
            if time < end_time and time > warning_time:
                return('warning', [end_time, end_time - time])
            elif time > end_time and time < end_time_close:
                return('overdue', [end_time, time - end_time])
            elif time > end_time_close:
                return('closed', [end_time, time - end_time])
            else:
                return(None, [None, None])
        else:
            return(None, [None, None])
    except Fair.DoesNotExist:
        return(None, [None, None])

