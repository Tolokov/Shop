from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Comment, Appeal_to_support, Category, Brand, Card_Product, Order
from .models import ProductImage, RatingGrade, Rating, Favorites, Cart, CartProduct


# Register your models here.


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
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'logo')

    # def get_image(self, obj):
    #     return mark_safe(f'<img src={obj.logo.url} width="50" height="60"')
    #
    # get_image.logo = "Изображение"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Card_Product)
class CardProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'product_public_ID',
        'price',
        'availability',
        'condition',
        'icon',
        'show_category',
        'brand',
    )
    search_fields = ('product_public_ID', 'name', 'description')
    list_filter = ('availability', 'condition', 'category', 'brand',)
    list_per_page = 50
    save_as = True
    list_editable = ('availability', 'condition')
    # поле обратной видимости в случае ManyToMany
    def show_category(self, categories):
        return "\n".join([cat.name for cat in categories.category.all()])




admin.site.register(Comment)
admin.site.register(Appeal_to_support)
admin.site.register(ProductImage)
admin.site.register(RatingGrade)
admin.site.register(Rating)
admin.site.register(Favorites)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
