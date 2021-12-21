from django.contrib import admin

from .models import News, Comment, Appeal_to_support, Category, Brand, Card_Product, Order
from .models import ProductImage, RatingGrade, Rating, Favorites, Cart, CartProduct
# Register your models here.

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Appeal_to_support)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Card_Product)
admin.site.register(ProductImage)
admin.site.register(RatingGrade)
admin.site.register(Rating)

admin.site.register(Favorites)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)



