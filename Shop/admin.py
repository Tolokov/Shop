from django.contrib import admin

from .models import News, Comment, Appeal_to_support, Category, Brand, Cart_Product
from .models import ProductImage, RatingGrade, Rating
# Register your models here.

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Appeal_to_support)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Cart_Product)
admin.site.register(ProductImage)
admin.site.register(RatingGrade)
admin.site.register(Rating)



