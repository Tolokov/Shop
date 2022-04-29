from django.contrib import admin

from Shop.models import *
from Shop.utils import GetImage

admin.site.site_title = 'Панель администрирования интернет магазина'
admin.site.site_header = 'Панель администрирования интернет магазина'

admin.site.register(Favorites)
admin.site.register(DefaultDelivery)
admin.site.register(RatingGrade)
admin.site.register(Order)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin, GetImage):
    list_display = ('name', 'get_count_brand_products', 'description', 'get_image')
    prepopulated_fields = {'slug': ('name',)}

    def get_count_brand_products(self, obj):
        return Card_Product.objects.filter(brand=obj).count()

    get_count_brand_products.short_description = 'Продуктов представлено брендом'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_count_category_products', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def get_count_category_products(self, obj):
        return Card_Product.objects.filter(category=obj).count()

    get_count_category_products.short_description = 'Продуктов в категории'


@admin.register(ProductImage)
class ProductImages(admin.ModelAdmin, GetImage):
    """Все изображения товара"""
    list_display = ('product', 'get_image')
    readonly_fields = ('get_image',)
    list_filter = ('product',)

    def show_product(self, obj):
        return '\n'.join([cat.name for cat in obj.product.all()])


class ProductImagesInline(admin.TabularInline, GetImage):
    model = ProductImage
    extra = 0
    readonly_fields = ('get_image',)


@admin.register(Card_Product)
class CardProductAdmin(admin.ModelAdmin, GetImage):
    """Карточка продукта"""
    list_per_page = 20
    save_as = True
    readonly_fields = ('get_image',)
    search_fields = ('product_public_ID', 'name', 'description')
    list_filter = ('availability', 'condition', 'category', 'brand',)
    save_on_top = True

    inlines = [ProductImagesInline]
    list_display = (
        'name',
        'product_public_ID',
        'price',
        'availability',
        'condition',
        'get_image',
        'show_category',
        'brand',
    )
    list_editable = ('availability', 'condition')
    fieldsets = (
        (None, {'fields': (('name', 'product_public_ID'),)}),
        (None, {'fields': (('price', 'availability', 'condition'),)}),
        ('Неизменяемые категории товаров', {'classes': ('collapse',), 'fields': (('brand', 'category'),)}),
        (None, {'fields': (('get_image', 'image'),)}),
        (None, {'fields': (('description',),)})
    )

    def show_category(self, obj):
        """поле обратной видимости в случае ManyToMany"""
        return '\n'.join([cat.name for cat in obj.category.all()])


@admin.register(Review)
class RatingGradeAdmin(admin.ModelAdmin):
    """Все оценки продукту"""
    list_display = ('name', 'ipaddress', 'email', 'created', 'product', 'update')


@admin.register(Cart)
class CartGradeAdmin(admin.ModelAdmin):
    """Корзина покупателя"""
    list_display = ('user', 'total', 'product')



# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'cart',
#         'name_first',
#         'name_last',
#         'phone',
#         'address',
#         'message',
#         'order_start',
#         'order_finish',
#         'status',
#         'buying_type',
#     )


