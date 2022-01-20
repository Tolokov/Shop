from django.urls import path
from Interactive import views

urlpatterns = [
    path('mail/', views.MailView.as_view(), name='mail'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('profile/', views.ProfileCreate.as_view(), name='profile'),
    path('delivery/', views.DeliveryFormView.as_view(), name='delivery'),
    path('delDelivery/', views.DeleteDelivery.as_view(), name='delDelivery')

]
