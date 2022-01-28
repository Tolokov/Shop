from django.urls import path, include
from django.views.decorators.cache import cache_page

from Blog import views


urlpatterns = [
    path('', cache_page(60 * 12)(views.BlogListView.as_view()), name='blog'),
    path('<int:post_id>/', views.BlogDetailView.as_view(), name='single_post'),
    path('comment/<int:pk>/', views.BlogDetailView.as_view(), name='single_post'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', views.SearchResultsListView.as_view(), name='search'),
]
