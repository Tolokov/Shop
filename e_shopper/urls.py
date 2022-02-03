from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('', include('Shop.urls')),
    path('', include('Interactive.urls')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += i18n_patterns(
    path('blog/', include('Blog.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
)

handler404 = 'e_shopper.handlers.ex404'
handler500 = 'e_shopper.handlers.ex500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
