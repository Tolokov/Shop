# from django.shortcuts import reverse
from django.urls import reverse

from django.db import models
from django.db.models import BooleanField, TextField, CharField, ImageField, DateField, TimeField
from django.db.models import CASCADE, SET_NULL

from datetime import date
from django.utils import timezone

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
        'self', verbose_name="Ответ на сообщение", on_delete=SET_NULL, blank=True, null=True
    )
    news = models.ForeignKey(News, on_delete=CASCADE)
    creator = models.ForeignKey(User, on_delete=CASCADE)
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
    creator = models.ForeignKey(User, on_delete=SET_NULL, null=True)

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
    slug = models.SlugField(max_length=160, unique=True)

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
    slug = models.SlugField(max_length=160, unique=True)
    logo = ImageField("Логотип", upload_to="media/brands/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Card_Product(models.Model):
    '''
    Карточка продукта
    '''
    product_public_ID = models.IntegerField(blank=False, primary_key=False, default=100000, unique=True)
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
    CONDITION_CHOICE = (
        (NEW, 'new'),
        (FRESH, 'fresh'),
        (SECOND_HAND, 'second hand'),
    )
    condition = models.CharField(
        max_length=1,
        choices=CONDITION_CHOICE,
        default=FRESH,
        blank=False,
    )

    icon = ImageField('Изображение в корзине', upload_to='media/product_icon')
    category = models.ManyToManyField(Category, verbose_name="категории")
    brand = models.ForeignKey(Brand, verbose_name="бренды", on_delete=SET_NULL, null=True, blank=False)

    def __str__(self):
        return f'ID: {self.product_public_ID} NAME: {self.name}'

    class Meta:
        verbose_name = 'Карточка продукта'
        verbose_name_plural = 'Карточки продуктов'
        ordering = ['product_public_ID']

    # Увеличивает счетчик product_public_ID на единицу, после сохраниния
    # def save(self, *args, **kwargs):
    #     self.product_public_ID = self.product_public_ID + 1
    #     super().save(*args, **kwargs) # Call the "real" save() method.




class ProductImage(models.Model):
    '''
    Изображения отображаемые с карточкой товара.
    '''
    title = models.CharField("Заголовок", max_length=100, blank=True)
    description = models.TextField("Описание", max_length=2000, blank=True)
    image = models.ImageField("Фотография товара", upload_to="media/")
    product = models.ForeignKey(Card_Product, verbose_name="Продукты", on_delete=CASCADE)

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
    creator = models.ForeignKey(User, on_delete=CASCADE, verbose_name="создатель")
    grade = models.ForeignKey(RatingGrade, on_delete=CASCADE, verbose_name="оценка")
    product = models.ForeignKey(Card_Product, on_delete=CASCADE, verbose_name="продукт")

    def __str__(self):
        return f'{self.product}, {self.grade}, {self.creator}'

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

# step 3

class CartProduct(models.Model):
    '''
    Выбранные пользователем товары
    '''
    user = models.ForeignKey(User, on_delete=CASCADE)
    products = models.ManyToManyField(Card_Product)

    class Meta:
        verbose_name = "Товар добавленный в корзину"
        verbose_name_plural = "Товары добавленные в корзину"



class Cart(models.Model):
    '''
    Корзина пользователя
    '''
    user = models.ForeignKey(User, on_delete=CASCADE)
    products = models.ForeignKey(CartProduct, on_delete=CASCADE, blank=True)
    total_product = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return (self.products)
    class Meta:
        verbose_name = 'Тележка'
        verbose_name_plural = 'Тележки'



class Favorites(models.Model):
    '''
    Избранное
    '''
    user = models.ForeignKey(User, on_delete=CASCADE)
    products = models.ManyToManyField(Card_Product)

    class Meta:
        verbose_name = "Товар добавленный в корзину"
        verbose_name_plural = "Товары добавленные в корзину"


class Order(models.Model):
    '''
    Заказ
    '''
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True,)

    first_name = models.CharField(max_length=350, verbose_name='Имя')
    last_name = models.CharField(max_length=350, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес', null=True, blank=True)
    message = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    order_start = models.DateTimeField(auto_now_add=True, verbose_name='Пполучен')
    order_finish = models.DateTimeField(verbose_name='Исполнен', default=timezone.now)

    STATUS_1 = 'created'
    STATUS_2 = 'in_progress'
    STATUS_3 = 'ready_to_receive'
    STATUS_4 = 'completed'
    STATUS_CHOICES = (
        (STATUS_1, 'Заказ получен'),
        (STATUS_2, 'Заказ обрабатывается'),
        (STATUS_3, 'Заказ готов к выдаче'),
        (STATUS_4, 'Заказ исполнен')
    )
    status = models.CharField(max_length=22, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_1)


    BUYING_SELF = 'self'
    BUYING_DELIVERY = 'delivery'
    BUYING_CHOICES = (
        (BUYING_SELF, 'Самовывоз'),
        (BUYING_DELIVERY, 'Доставка')
    )
    buying_type = models.CharField(max_length=22, verbose_name='Тип заказа', choices=BUYING_CHOICES, default=BUYING_SELF)


    def __str__(self):
        return f'{self.user}, {self.cart}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'




# # step 4
# class Promo(models.Model):
#     '''
#     Промокоды, скидки и подарочные сертификаты
#     '''
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
# class Cart_Supplier(models.Model):
#     '''
#     Тележка товаров пользователя, с последующим добавлением к количеству каждого товара
#     '''
