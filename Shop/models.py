from django.db import models
from django.db.models import CASCADE, SET_NULL, F, Sum
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils import timezone
from decimal import Decimal

from Interactive.models import Delivery


class Category(models.Model):
    """Категории продуктов"""
    name = models.CharField("Название категории", max_length=150)
    description = models.TextField("Описание", max_length=1500, blank=True)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Brand(models.Model):
    """Производитель продукта"""
    name = models.CharField("Название бренда", max_length=150)
    description = models.TextField("Описание", max_length=1500)
    slug = models.SlugField(max_length=160, unique=True)
    image = models.ImageField("Логотип", upload_to="media/brands/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Card_Product(models.Model):
    """Карточка продукта"""
    product_public_ID = models.IntegerField(primary_key=False, unique=True, null=False, default=1111111)
    name = models.CharField(max_length=300)
    description = models.TextField(max_length=5000)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    availability = models.BooleanField(default=True, verbose_name='hidden')
    quantity = models.PositiveIntegerField('На складе', default=0)

    NEW = 'new'
    FRESH = 'fresh'
    SECOND_HAND = 'hand'
    CONDITION_CHOICE = (
        (NEW, 'new'),
        (FRESH, 'fresh'),
        (SECOND_HAND, 'hand'),
    )
    condition = models.CharField(
        max_length=5,
        choices=CONDITION_CHOICE,
        default=FRESH,
        blank=False,
    )

    image = models.ImageField('Изображение в корзине', upload_to='media/product_icon', null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name="категории")
    brand = models.ForeignKey(Brand, verbose_name="бренды", on_delete=SET_NULL, null=True, blank=False)

    def __str__(self):
        return f'ID: {self.product_public_ID} NAME: {self.name}'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_ID': self.id})

    class Meta:
        verbose_name = 'Карточка продукта'
        verbose_name_plural = 'Карточки продуктов'
        ordering = ['product_public_ID']


class ProductImage(models.Model):
    """Изображения отображаемые с карточкой товара на галерее изображений"""
    title = models.CharField("Заголовок", max_length=100, blank=True)
    description = models.TextField("Описание", max_length=2000, blank=True)
    image = models.ImageField("Фотография товара", upload_to="media/")
    product = models.ForeignKey(Card_Product, verbose_name="Продукты", on_delete=CASCADE)

    def __str__(self):
        return f'{self.title if len(self.title) > 2 else "нет заголовка"} {self.product}'

    class Meta:
        verbose_name = 'Фотография к товару'
        verbose_name_plural = 'Фотографии к товару'


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(User, on_delete=CASCADE)
    product = models.ForeignKey(Card_Product, on_delete=CASCADE, blank=True)
    total = models.PositiveIntegerField(default=1)

    @staticmethod
    def total_price(user_pk):
        """запрос в базу данных о стоимости всех товаров в корзине пользователя"""
        total = Cart.objects.filter(user=user_pk).aggregate(
            total_price=Sum(F('total') * F('product__price'))
        )['total_price'] or Decimal('0')
        return total

    @property
    def product_cost(self):
        """Стоимость всех идентичных товаров добавленных в корзину"""
        total = self.total * self.product.price
        return total

    def __str__(self):
        return f'{self.product}, {self.user}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = (('user', 'product'),)


class Favorites(models.Model):
    """Избранное пользователя"""
    user = models.ForeignKey(User, on_delete=CASCADE)
    products = models.ForeignKey(Card_Product, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user}, {self.products}'

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = (("user", "products"),)


class Order(models.Model):
    """Заказ пользователя"""
    user = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True, )

    name_first = models.CharField(max_length=350, verbose_name='Имя')
    name_last = models.CharField(max_length=350, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес', null=True, blank=True)
    message = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    order_start = models.DateTimeField(auto_now_add=True, verbose_name='Получен')
    order_finish = models.BooleanField(verbose_name='Исполнен', default=False)

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
    buying_type = models.CharField(
        max_length=22, verbose_name='Тип заказа', choices=BUYING_CHOICES, default=BUYING_SELF
    )

    def __str__(self):
        return f'{self.user}, {self.cart}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class DefaultDelivery(models.Model):
    """Отображаемый по умолчанию <адрес доставки>(Interactive.Delivery) для каждого пользователя"""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    default = models.OneToOneField(Delivery, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user}, {self.default}'

    class Meta:
        verbose_name = 'Адрес по умолчанию'
        verbose_name_plural = 'Адреса по умолчанию'


class RatingGrade(models.Model):
    """Отображаемые значения рейтинга (от 1 до 5)"""
    value = models.PositiveSmallIntegerField("Рейтинг", default=3)

    def __str__(self):
        return f'{self.value}'

    def get_value(self):
        return range(self.value)

    class Meta:
        verbose_name = 'Отображаемое значение рейтинга'
        verbose_name_plural = 'Отображаемые значения рейтинга'


class Review(models.Model):
    """Отзывы к продуктам"""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    update = models.DateTimeField(auto_now=True, blank=True)

    ipaddress = models.CharField('IP адрес', max_length=15)
    product = models.ForeignKey(Card_Product, verbose_name='Продукт', on_delete=CASCADE)
    grade = models.ForeignKey(RatingGrade, on_delete=CASCADE, verbose_name="оценка", blank=True)

    def __str__(self):
        return f'{self.product}, {self.name}, {self.ipaddress}'

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'
        ordering = ['created']



# class Promo(models.Model):
#     """
#     Промокоды, скидки и подарочные сертификаты
#     """
#
# class Currency(models.Model):
#     """
#     Курс валют
#     """
#
# class Notification(models.Model):
#     """Уведомления"""
#     recipient = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Получатель')
#     text = models.TextField()
#     read = models.BooleanField(default=False)
#     objects = NotificationManager()
#
#     def __str__(self):
#         return f"Уведомление для {self.recipient.user.username} | id={self.id}"
#
#     class Meta:
#         verbose_name = 'Уведомление'
#         verbose_name_plural = 'Уведомления'
