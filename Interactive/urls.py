from django.urls import path, include
from Interactive import views


urlpatterns = [
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileCreate.as_view(), name='profile'),

]
