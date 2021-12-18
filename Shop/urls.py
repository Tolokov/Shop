from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Shop import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('<int:post_id>/', views.SinglePostVies.as_view(), name='single_post'),

    path('cart/', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('product-detail/', views.Product_detailView.as_view(), name='product_detail'),
    path('favorites/', views.Product_detailView.as_view(), name='favorites'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


