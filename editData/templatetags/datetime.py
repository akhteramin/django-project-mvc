from django import template
import time

register = template.Library()

@register.filter
def get_date_time(value, arg):
    # timestamp = "2008-09-26T01:51:42.000Z"
    ts = time.strptime(value[:19], "%Y-%m-%dT%H:%M:%S")
    time.strftime("%d/%m/%Y %H:%M:%S", ts)

    return time.strftime("%d/%m/%Y %H:%M", ts)