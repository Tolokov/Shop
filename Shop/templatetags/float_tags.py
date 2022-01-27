from django import template
from django.template.defaultfilters import floatformat

register = template.Library()


def formatted_float(value):
    value = floatformat(value, arg=4)
    return str(value).replace(',', '.')[:-2]


register.filter('formatted_float', formatted_float)
