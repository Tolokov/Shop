from django.urls import path, include
from Interactive import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
