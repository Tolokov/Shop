from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Shop.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

handler404 = 'Shop.views.ex404'
