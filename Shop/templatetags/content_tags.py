from django import template
from ..models import *

register = template.Library()

@register.simple_tag()
def get_categories():
    categories = Category.objects.order_by('name')
    return categories


@register.simple_tag()
def filter_categories(category_id=1, count=4):
    product = Card_Product.objects.filter(category__id=category_id)[:count]
    return product
    #     {
    #     'categories_products': product,
    #     # 'category_selected': category_selected,
    # }



# @register.inclusion_tag('content/category_products.html')
# def filter_categories(category_selected=2, count=4):
#     product = 2
#     # if category_selected:
#     #     product = {'price': '12'}
#     #     # products = Card_Product.objects.all()[:count]
#     # else:
#     #     product = {'price': '12'}
#
#     return {
#         'categories_products': product,
#         'category_selected': category_selected,
#     }


