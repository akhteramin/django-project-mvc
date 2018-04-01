from django import template
import time
from mysite.settings import APP_LIST, APP_URL

register = template.Library()

@register.filter
def get_app_name(value, arg):
    # timestamp = "2008-09-26T01:51:42.000Z"

    return APP_LIST[str(value)]

@register.filter
def get_app_url(value, arg):
    # timestamp = "2008-09-26T01:51:42.000Z"

    return APP_URL[str(value)]