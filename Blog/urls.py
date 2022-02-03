from django.urls import path, include

from Blog import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog'),
    path('<int:post_id>/', views.BlogDetailView.as_view(), name='single_post'),
    path('comment/<int:pk>/', views.BlogDetailView.as_view(), name='single_post'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', views.SearchResultsListView.as_view(), name='search'),
]
