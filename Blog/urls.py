from django.urls import path
from Blog import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog'),
    path('<int:post_id>/', views.BlogDetailView.as_view(), name='single_post'),
    path('comment/<int:pk>/', views.BlogDetailView.as_view(), name='single_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
