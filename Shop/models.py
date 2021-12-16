from django.db import models


# step 1
class User(models.Model):
    '''
    Учетная пользователя после регистрации
    '''


class News_and_event(models.Model):
    '''
    Посты с новостями и событиями, которые может оставлять только зарегистрированный пользователь
    '''


class Comment(models.Model):
    '''
    Комментарии к ивентам, новостям и другим комментариям, реализовать связь.
    '''


class Appeal_to_support(models.Model):
    '''
    Сообщение пользователя в тех.поддержку(реализовать без моделей)
    '''



# step 2
class Card_Product(models.Model):
    '''
    Карточка продукта
    '''


class Category(models.Model):
    '''
    Многие ко многим
    '''


class Brand(models.Model):
    '''
    Один ко многим
    '''


class Product_Image(models.Model):
    '''
    Изображения отображаемые с карточкой товара.
    '''


class Rating(models.Model):
    '''
    Рейтинг выставленный продукту
    '''


class Rating_star(models.Model):
    '''
    Отображаемые значения рейтинга
    '''


# step 3
class Cart(models.Model):
    '''
    Корзина пользователя
    '''


class Cart_product(models.Model):
    '''
    Выбранные пользователем товары
    '''


class Favorites(models.Model):
    '''
    Избранное
    '''


class Cart_favorites(models.Model):
    '''
    Товары добавленные пользователем в избранное
    '''


class Product(models.Model):
    '''
    Все продукты
    '''


# step 4
class Promo(models.Model):
    '''
    Промокоды, скидки и подарочные сертификаты
    '''


class Order(models.Model):
    '''
    Заказ
    '''


class Currency(models.Model):
    '''
    Курс валют
    '''


# step 5
class Supplier(models.Model):
    '''
    Поставщик товара, заполняется зарегистрированным пользователем
    '''


class Cart_Supplier(models.Model):
    '''
    Тележка товаров пользователя, с последующим добавлением к количеству каждого товара
    '''
