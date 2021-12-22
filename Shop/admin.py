from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Comment, Appeal_to_support, Category, Brand, Card_Product, Order
from .models import ProductImage, RatingGrade, Rating, Favorites, Cart, CartProduct

admin.site.site_title = 'Панель администрирования интернет магазина'
admin.site.site_header = 'Панель администрирования интернет магазина'


class GetImage:

    def get_logo(self, obj):
        return mark_safe(f'<img src={obj.logo.url} width="100%" height="80"')

    def get_icon(self, obj):
        return mark_safe(f'<img src={obj.icon.url} width="100" height="80"')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="80"')

    get_image.short_description = "Логотип"
    get_icon.short_description = "Изображение"


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'draft', 'poster', 'creator',)
    list_filter = ('creator', 'draft',)
    search_fields = ('title', 'description')
    save_as = True
    save_as_continue = False
    list_per_page = 30
    actions_on_bottom = True
    list_editable = ('draft',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin, GetImage):
    list_display = ('name', 'description', 'get_logo')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')



@admin.register(ProductImage)
class ProductImages(admin.ModelAdmin, GetImage):
    list_display = ('product', 'get_image')
    list_filter = ('product',)

    def show_product(self, obj):
        return "\n".join([cat.name for cat in obj.product.all()])


# class ProductImagesInline(admin.StackedInline):
#     model = ProductImage
#     extra = 3


@admin.register(Card_Product)
class CardProductAdmin(admin.ModelAdmin, GetImage):
    list_per_page = 50
    save_as = True
    readonly_fields = ('get_icon',)
    search_fields = ('product_public_ID', 'name', 'description')
    list_filter = ('availability', 'condition', 'category', 'brand',)

    # inlines = [ProductImagesInline]
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
        ('Не изменяемые категории товаров',
         {
             'classes': ('collapse',),
             'fields': (('brand', 'category'),)
         }),
        (None,
         {
             'fields': (('get_icon',),)
         })
    )

    # поле обратной видимости в случае ManyToMany
    def show_category(self, obj):
        return "\n".join([cat.name for cat in obj.category.all()])


admin.site.register(Comment)
admin.site.register(Appeal_to_support)
admin.site.register(RatingGrade)
admin.site.register(Rating)
admin.site.register(Favorites)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
