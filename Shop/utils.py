from django.urls import reverse_lazy
from django.shortcuts import redirect

from Shop.models import Card_Product, Category, Brand


class DataMixin:
    model = Card_Product
    context_object_name = 'products'

    def get_categories(self):
        return Category.objects.all().values('id', 'name')

    def get_brands(self):
        return Brand.objects.all().prefetch_related('card_product_set')

    def post(self, request, **kwargs):
        print('Добавление в корзину')
        print(kwargs)
        print(request.user.id)
        print(self.__class__())
        return redirect(reverse_lazy('shop'))

    # from math import ceil, floor
    # from django.db.models import Max, Min
    # def get_price_min(self):
    #     return floor(Card_Product.objects.aggregate(Min('price'))['price__min'])
    #
    # def get_price_max(self):
    #     return ceil(Card_Product.objects.aggregate(Max('price'))['price__max'])

