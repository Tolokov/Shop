from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('Shop.urls')),
    path('', include('Interactive.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('blog/', include('Blog.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
]

handler404 = 'Interactive.views.ex404'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
