from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firs_name = models.CharField(max_length=150,  null=True)
    last_name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150, null=True)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True, default='media/avatars/orange.jpg')

    def __str__(self):
        return f'{self.user}'


class Delivery(models.Model):
    """Адрес доставки"""
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.SET_NULL, null=True)
    address_header = models.CharField(verbose_name='односложный заголовок адреса доставки', max_length=500, blank=True)
    email = models.EmailField(max_length=254, blank=True, default='User.email')
    notification_on_email = models.BooleanField(default=True)

    name_first = models.CharField(default='User.first_name', max_length=500, verbose_name='Имя', blank=True)
    name_last = models.CharField(default='User.last_name', max_length=500, verbose_name='Фамилия', blank=True)

    address = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    state = models.CharField(max_length=500)

    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    sub_phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20, blank=True)
    comment = models.TextField()

    def __str__(self):
        return self.address_header

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

