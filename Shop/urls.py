from django.urls import path
from Shop import views


urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('products/<int:product_ID>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('review/<int:pk>/', views.ProductDetailView.as_view(), name="product_detail"),
    path('filter/', views.FilterProductView.as_view(), name="filter"),
    path('shop/', views.ShopListView.as_view(), name='shop'),

    path('delivery/', views.DeliveryFormView.as_view(), name='delivery'),

    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('add_favorites/<int:product_id>', views.AddFavoritesView.as_view(), name='addFavorites'),
    path('del_favorites/<int:product_id>', views.DeleteFavoritesView.as_view(), name='delFavorites'),

    path('cart/<int:product_id>', views.FavoritesView.as_view(), name='addCart'),

    path('cart/', views.CartView.as_view(), name='cart'),
]