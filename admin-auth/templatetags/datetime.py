from django import template
import time

register = template.Library()

@register.filter
def get_date_time(value, arg):
    # timestamp = "2008-09-26T01:51:42.000Z"
    ts = time.strptime(value[:19], "%Y-%m-%dT%H:%M:%S")
    time.strftime("%m/%d/%Y %H:%M:%S", ts)
    print(value)
    print(time.strftime("%m/%d/%Y %H:%M", ts))
    return time.strftime("%m/%d/%Y %H:%M", ts)