from django.urls import path
from rest_framework import routers

from Shop import views
from Shop.api import CardViewSet

from Shop.utils import global_exception_decorator as g

router = routers.DefaultRouter()
router.register('api/card', CardViewSet, 'card_product')


urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),

    path('shop/', g(views.ShopListView.as_view()), name='shop'),
    path('products/<int:product_ID>/', g(views.ProductDetailView.as_view()), name='product_detail'),
    path('review/', g(views.ProductDetailView.as_view()), name="add_review"),
    path('json-filter/', g(views.JsonFilterProductView.as_view()), name='json_filter'),

    path('cart/', g(views.CartListView.as_view()), name='cart'),
    path('add_cart/<int:product_id>', g(views.AddCart.as_view()), name='addCart'),
    path('off_cart/<int:product_id>', g(views.PopCart.as_view()), name='popCart'),
    path('del_cart/<int:product_id>', g(views.DeleteCartProduct.as_view()), name='deleteCart'),

    path('favorites/', g(views.FavoritesView.as_view()), name='favorites'),
    path('add_favorites/<int:product_id>', g(views.AddFavoritesView.as_view()), name='addFavorites'),
    path('del_favorites/<int:product_id>', g(views.DeleteFavoritesView.as_view()), name='delFavorites'),

    path('order/', g(views.OrderListView.as_view()), name='order'),
    path('order/<int:id>/', g(views.OrderListView.as_view()), name='choice'),

]

urlpatterns += router.urls
