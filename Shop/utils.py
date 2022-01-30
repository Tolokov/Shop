from django.utils.safestring import mark_safe
from django.db.models import Count

from Shop.models import Card_Product, Category, Brand


class MixinForMainPages:
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

    @staticmethod
    def cut_queryset(queryset, step=3) -> list:
        """ Режет queryset на блоки для отображения на странице [[img,img,img.], [...], ...] """
        result = list()
        for i in range(0, len(queryset), step):
            result.append(queryset[i:i + step])
        return result

    def get_recommended_queryset(self, queryset, context: dict, how_much_to_display_on_main=4) -> dict:
        """Список карточек товаров отсортированные по количеству отзывов, отображаются на главной странице"""
        recommended = queryset.annotate(cnt=Count('review')).order_by('-cnt')
        recommended_queryset = self.cut_queryset(recommended.values('name', 'price', 'image', 'id', 'condition'), 3)
        first_block_of_cards = recommended_queryset[0]
        next_blocks_of_cards = recommended_queryset[1:how_much_to_display_on_main]
        result = (first_block_of_cards, next_blocks_of_cards)
        context['recommended_item'] = result[0]
        context['recommended_next_items'] = result[1]
        return context


class GetImage:
    """Вывод изображений в административную панель"""

    def get_image(self, obj):
        print('get_image', obj)
        return mark_safe(f'<img src={obj.image.url} width="100" height="80"')

    get_image.short_description = 'Изображение'


