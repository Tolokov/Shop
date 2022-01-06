from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Shop.urls')),
    path('blog/', include('Blog.urls')),
    path('', include('Interactive.urls')),
]

handler404 = 'Shop.views.ex404'
