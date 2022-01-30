from django.utils.safestring import mark_safe

from Shop.models import Card_Product, Category, Brand


class DataMixin:
    model = Card_Product
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Действия происходят на странице каталога продуктов"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['shop_selected'] = 'active'
        return context

    @staticmethod
    def get_categories():
        """Отображение всех категорий на странице каталога продуктов"""
        return Category.objects.all().values('id', 'name')

    @staticmethod
    def get_brands():
        """Отображение всех брендов на странице каталога продуктов"""
        return Brand.objects.all().prefetch_related('card_product_set')


class GetImage:
    """Вывод изображений в административную панель"""

    def get_image(self, obj):
        print('get_image', obj)
        return mark_safe(f'<img src={obj.image.url} width="100" height="80"')

    get_image.short_description = 'Изображение'
