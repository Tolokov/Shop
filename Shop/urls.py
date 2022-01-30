from django.urls import path
from rest_framework import routers

from Shop import views
from Shop.api import CardViewSet


router = routers.DefaultRouter()
router.register('api/card', CardViewSet, 'card_product')


urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),

    path('shop/', views.ShopListView.as_view(), name='shop'),
    path('products/<int:product_ID>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('review/', views.ProductDetailView.as_view(), name="add_review"),
    path('json-filter/', views.JsonFilterProductView.as_view(), name='json_filter'),

    path('cart/', views.CartListView.as_view(), name='cart'),
    path('add_cart/<int:product_id>', views.AddCart.as_view(), name='addCart'),
    path('off_cart/<int:product_id>', views.PopCart.as_view(), name='popCart'),
    path('del_cart/<int:product_id>', views.DeleteCartProduct.as_view(), name='deleteCart'),

    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('add_favorites/<int:product_id>', views.AddFavoritesView.as_view(), name='addFavorites'),
    path('del_favorites/<int:product_id>', views.DeleteFavoritesView.as_view(), name='delFavorites'),

    path('order/', views.OrderListView.as_view(), name='order'),
    path('order/<int:id>/', views.OrderListView.as_view(), name='choice'),

]

urlpatterns += router.urls
