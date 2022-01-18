from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    """ Создание модели Покупателя после регистрации"""
    if created:
        Customer.objects.create(user=instance)
    else:
        try:
            instance.customer.save()
        except ObjectDoesNotExist:
            Customer.objects.create(user=instance)


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    first_name = models.CharField(max_length=150, null=True, default='')
    last_name = models.CharField(max_length=150, null=True, default='')
    phone = models.CharField(max_length=150, null=True, default='')
    email = models.CharField(max_length=150, null=True, default='')
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True, default='media/avatars/orange.jpg')

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Mail(models.Model):
    """Электронные адреса пользователей подписавшихся на рассылку"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Список электронных адресов'
        verbose_name_plural = 'Список электронных адресов'


class Delivery(models.Model):
    """Адрес доставки"""
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.SET_NULL, null=True)
    address_header = models.CharField('Заголовок адреса доставки', max_length=500, blank=False)
    email = models.EmailField('Email', max_length=254)
    notification_on_email = models.BooleanField('Получать уведомления по Email', default=True)

    name_first = models.CharField(default='', max_length=500, verbose_name='Имя', blank=True)
    name_last = models.CharField(default='', max_length=500, verbose_name='Фамилия', blank=True)

    address = models.CharField('Адрес', max_length=500)
    country = models.CharField('Страна', max_length=500)
    state = models.CharField('Штат/Регион', max_length=500)

    zip = models.CharField('Индекс', max_length=10, blank=True)
    phone = models.CharField('Номер телефона', max_length=20)
    sub_phone = models.CharField('Дополнительный номер телефона', max_length=20, blank=True)
    comment = models.TextField('Дополнительный комментарий к доставке', blank=True)

    def __str__(self):
        return self.address_header

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
        unique_together = (('user', 'address_header'),)
