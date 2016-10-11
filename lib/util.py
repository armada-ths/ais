import time


def unix_time(datetime):
    return int(time.mktime(datetime.timetuple()))
