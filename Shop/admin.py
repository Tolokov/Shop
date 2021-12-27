from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

admin.site.site_title = 'Панель администрирования интернет магазина'
admin.site.site_header = 'Панель администрирования интернет магазина'


class GetImage:

    def get_logo(self, obj):
        return mark_safe(f'<img src={obj.logo.url} width="100%" height="80"')

    def get_icon(self, obj):
        return mark_safe(f'<img src={obj.icon.url} width="100" height="80"')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="80"')

    get_image.short_description = 'Логотип'
    get_icon.short_description = 'Изображение'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    '''
    Новости и события
    '''
    list_display = ('title', 'date', 'time', 'draft', 'poster', 'creator',)
    list_filter = ('creator', 'draft',)
    search_fields = ('title', 'description')
    save_as = True
    save_as_continue = False
    list_per_page = 30
    actions_on_bottom = True
    save_on_top = True
    list_editable = ('draft',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin, GetImage):
    list_display = ('name', 'get_count_brand_products', 'description', 'get_logo')
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
    '''
    Все второстепенные изображения товара
    '''
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
    '''
    Карточка продукта
    '''
    list_per_page = 50
    save_as = True
    readonly_fields = ('get_icon',)
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
        'get_icon',
        'show_category',
        'brand',
    )
    list_editable = ('availability', 'condition')
    fieldsets = (
        (None,
         {
             'fields': (('name', 'product_public_ID'),)
         }),
        (None,
         {
             'fields': (('price', 'availability', 'condition'),)
         }),
        ('Неизменяемые категории товаров',
         {
             'classes': ('collapse',),
             'fields': (('brand', 'category'),)
         }),
        (None,
         {
             'fields': (('get_icon', 'icon'),)
         }),
        (None,
         {
             'fields': (('description',),)
         })
    )

    # поле обратной видимости в случае ManyToMany
    def show_category(self, obj):
        return '\n'.join([cat.name for cat in obj.category.all()])


# \\\\\\\
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('creator', 'text', 'parent', 'news')
    readonly_fields = ('creator',)



@admin.register(RatingGrade)
class RatingAdmin(admin.ModelAdmin):
    '''Итоговый рейтинг'''
    list_display = ('value',)


@admin.register(Rating)
class RatingGradeAdmin(admin.ModelAdmin):
    '''Все оценки продукту'''
    list_display = ('creator', 'grade', 'product')


@admin.register(Cart)
class CartGradeAdmin(admin.ModelAdmin):
    '''Корзина покупателя'''
    list_display = ('user', 'total_product', 'total_price', 'products')
    # def show_products(self, obj):
    #     return '\n'.join([cat.name for cat in obj.products.all()])


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    '''Избранное'''
    list_display = ('user', 'show_products')

    def show_products(self, obj):
        return '\n'.join([cat.name for cat in obj.products.all()])


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show_products')

    def show_products(self, obj):
        return ', '.join([cat.name for cat in obj.products.all()])


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'cart',
        'first_name',
        'last_name',
        'phone',
        'address',
        'message',
        'order_start',
        'order_finish',
        'status',
        'buying_type',
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('address_header', 'user', 'email')



