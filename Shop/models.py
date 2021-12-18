# from django.shortcuts import reverse
from django.urls import reverse

from django.db import models
from django.db.models import BooleanField, TextField, CharField, ImageField, DateField, TimeField

from datetime import date

# step 1
class User(models.Model):
    '''
    Учетная запись пользователя после регистрации
    '''
    pass



class News(models.Model):
    '''
    Посты с новостями и событиями, которые может оставлять только зарегистрированный пользователь
    '''
    title = CharField('Заголовок', max_length=150)
    description = TextField('Описание', max_length=5000)
    date = DateField('Дата создания', default=date.today)
    time = TimeField('Время создания', auto_now=True, null=True)
    draft = BooleanField('Черновик', default=False)
    poster = ImageField('Постер', upload_to='media/poster/')
    creator = CharField('Создатель', max_length=150, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_post', kwargs={'post_id': self.id})


    class Meta:
        verbose_name = 'Новость или событие'
        verbose_name_plural = 'Новости и события'



# \\\\\


class Comment(models.Model):
    '''
    Комментарии к ивентам, новостям и другим комментариям, реализовать связь.
    '''
    text = models.TextField("Сообщение", max_length=1500)
    parent = models.ForeignKey(
        'self', verbose_name="Ответ на сообщение", on_delete=models.SET_NULL, blank=True, null=True
    )
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)



class Appeal_to_support(models.Model):
    '''
    Сообщение пользователя в тех.поддержку(реализовать без моделей)
    '''
    text = TextField("Сообщение", max_length=1500)
    date = DateField('Дата создания', default=date.today)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)






#
# # step 2
# class Card_Product(models.Model):
#     '''
#     Карточка продукта
#     '''
#
#
# class Category(models.Model):
#     '''
#     Многие ко многим
#     '''
#
#
# class Brand(models.Model):
#     '''
#     Один ко многим
#     '''
#
#
# class Product_Image(models.Model):
#     '''
#     Изображения отображаемые с карточкой товара.
#     '''
#
#
# class Rating(models.Model):
#     '''
#     Рейтинг выставленный продукту
#     '''
#
#
# class Rating_star(models.Model):
#     '''
#     Отображаемые значения рейтинга
#     '''
#
#
# # step 3
# class Cart(models.Model):
#     '''
#     Корзина пользователя
#     '''
#
#
# class Cart_product(models.Model):
#     '''
#     Выбранные пользователем товары
#     '''
#
#
# class Favorites(models.Model):
#     '''
#     Избранное
#     '''
#
#
# class Cart_favorites(models.Model):
#     '''
#     Товары добавленные пользователем в избранное
#     '''
#
#
# class Product(models.Model):
#     '''
#     Все продукты
#     '''
#
#
# # step 4
# class Promo(models.Model):
#     '''
#     Промокоды, скидки и подарочные сертификаты
#     '''
#
#
# class Order(models.Model):
#     '''
#     Заказ
#     '''
#
#
# class Currency(models.Model):
#     '''
#     Курс валют
#     '''
#
#
# # step 5
# class Supplier(models.Model):
#     '''
#     Поставщик товара, заполняется зарегистрированным пользователем
#     '''
#
#
# class Cart_Supplier(models.Model):
#     '''
#     Тележка товаров пользователя, с последующим добавлением к количеству каждого товара
#     '''
