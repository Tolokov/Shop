from django import template
from ..models import *

register = template.Library()

@register.simple_tag()
def get_categories():
    categories = Category.objects.order_by('name')
    return categories

