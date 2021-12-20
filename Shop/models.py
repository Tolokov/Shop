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

    def get_prev_absolute_url(self):
        prev_page = self.id - 1
        return reverse('single_post', kwargs={'post_id': prev_page})

    def get_next_absolute_url(self):
        next_page = self.id + 1
        return reverse('single_post', kwargs={'post_id': next_page})

    class Meta:
        verbose_name = 'Новость или событие'
        verbose_name_plural = 'Новости и события'


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
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Appeal_to_support(models.Model):
    '''
    Сообщение пользователя в тех.поддержку(реализовать без моделей)
    '''
    text = TextField("Сообщение", max_length=1500)
    date = DateField('Дата создания', default=date.today)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"


# step 2
class Category(models.Model):
    '''
    Многие ко многим
    '''
    name = models.CharField("Название категории", max_length=150)
    description = models.TextField("Описание", max_length=1500, blank=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"



class Brand(models.Model):
    '''
    Один ко многим
    '''
    name = models.CharField("Название бренда", max_length=150)
    description = models.TextField("Описание", max_length=1500)
    url = models.SlugField(max_length=160, unique=True)
    logo = ImageField("Логотип", upload_to="media/brands/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Cart_Product(models.Model):
    '''
    Карточка продукта
    '''
    product_public_ID = models.IntegerField(blank=False, primary_key=False, max_length=6, default=100000, unique=True,)
    # public_ID = models.AutoField(
        # auto_created=True,
        # primary_key=False,
        # blank=False,
        # default=100000,
        # unique=True,
        # null=False,
    # )
    name = CharField(max_length=300)
    description = TextField(max_length=5000)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    availability = BooleanField(default=True, verbose_name='hidden')

    NEW = 'N'
    FRESH = 'F'
    SECOND_HAND = 'S'
    CONDITION_CHOICE = [
        (NEW, 'new'),
        (FRESH, 'fresh'),
        (SECOND_HAND, 'second hand'),
    ]
    condition = models.CharField(
        max_length=1,
        choices=CONDITION_CHOICE,
        default=FRESH,
        blank=False,
    )

    icon = ImageField('Изображение в корзине', upload_to='media/product_icon')
    category = models.ManyToManyField(Category, verbose_name="категории")
    brand = models.ForeignKey(Brand, verbose_name="бренды", on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return f'ID: {self.product_public_ID} NAME: {self.name}'

    class Meta:
        verbose_name = 'Карточка продукта'
        verbose_name_plural = 'Карточки продуктов'
        ordering = ['product_public_ID']


class ProductImage(models.Model):
    '''
    Изображения отображаемые с карточкой товара.
    '''
    title = models.CharField("Заголовок", max_length=100, blank=True)
    description = models.TextField("Описание", max_length=2000, blank=True)
    image = models.ImageField("Фотография товара", upload_to="media/")
    product = models.ForeignKey(Cart_Product, verbose_name="Продукты", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title if len(self.title) > 2 else "нет заголовка"} {self.product}'

    class Meta:
        verbose_name = 'Фотография к товару'
        verbose_name_plural = 'Фотографии к товару'


class RatingGrade(models.Model):
    '''
    Отображаемые значения рейтинга
    '''
    value = models.SmallIntegerField("Рейтинг", default=0)

    def __str__(self):
        return f' Текущая оценка продукта{self.value}'

    class Meta:
        verbose_name = 'отображаемое значение рейтинга'
        verbose_name_plural = 'Отображаемые значения рейтинга'


class Rating(models.Model):
    '''
    Рейтинг выставленный продукту
    '''
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="создатель")
    grade = models.ForeignKey(RatingGrade, on_delete=models.CASCADE, verbose_name="оценка")
    product = models.ForeignKey(Cart_Product, on_delete=models.CASCADE, verbose_name="продукт")

    def __str__(self):
        return f'{self.product}, {self.grade}, {self.creator}'

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

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
