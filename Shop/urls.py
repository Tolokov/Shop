from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Shop import views
from .views import SignUpView


urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<int:post_id>/', views.BlogDetailView.as_view(), name='single_post'),
    # path('<int:product_public_ID>', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_public_ID>/', views.ProductDetailView.as_view(), name='product_detail'),




    path('signup/', SignUpView.as_view(), name='signup'),
    path('delivery/', views.DeliveryView.as_view(), name='delivery'),

    path('cart/', views.CartView.as_view(), name='cart'),

    path('contact/', views.ContactView.as_view(), name='contact'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('product-detail/', views.ProductDetailView.as_view(), name='product_detail'),
    path('favorites/', views.ProductDetailView.as_view(), name='favorites'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


