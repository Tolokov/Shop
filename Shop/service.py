from django.core import serializers, paginator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Avg
from django.db import IntegrityError

from json import loads
from Shop.utils import timer

from Shop.models import Review, User, Card_Product, Favorites, Cart, DefaultDelivery, Delivery, Order, BuyProduct



class JsonHandler:

    def handler(self):
        """Обработчик поступающих запросов к ajax фильтру"""
        if self.request.GET == {}:
            return self.queryset[:18]

        elif len(self.request.GET) == 2:
            queryset = self.queryset.filter(
                Q(category__in=self.request.GET.getlist("category")) &
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset

        else:
            queryset = self.queryset.filter(
                Q(category__in=self.request.GET.getlist("category")) |
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset

    @timer
    def serialization(self, queryset):
        """Функция работает: 0:00:02.334938, нужна замена сериализатора"""
        return serializers.serialize("json", queryset)

    @timer
    def json_load(self, queryset_str):
        """Функция работает: 0:00:00.001000"""
        return loads(queryset_str)

    def json_answer(self):
        """Иза ошибки форимирования json ответа, пришлось воспользоваться встроенной библиотекой json"""
        queryset = self.get_queryset()
        serialized = self.serialization(queryset)
        json_loaded = self.json_load(serialized)
        return json_loaded


class ProductDetailMixin:

    def get_review_queryset(self, context: dict) -> dict:
        """Формирование средней оценки для продукта на основе оставленных отзывов"""
        review_queryset = Review.objects.filter(product=self.object).select_related('grade')
        context['reviews'] = review_queryset
        context['count'] = review_queryset.__len__()

        if review_queryset:
            avg = review_queryset.aggregate(Avg('grade__value'))['grade__value__avg']
            stars = round(avg)
            context['grade_on'] = range(stars)
            context['grade_off'] = range(5 - stars)
        else:
            context['avg_grade'] = False

        return context

    @staticmethod
    def paginator_optimization(queryset, per_page=3, max_pages=5):
        """Paginator optimization (4 SQL queries --> 1 SQL queries)"""
        list_objects = list(queryset[:per_page * max_pages])
        paginator_object = paginator.Paginator(list_objects, per_page=per_page)
        return paginator_object

    @staticmethod
    def get_user_ip(request):
        """Получение ip пользователя оставившего комментарий"""
        redirected = request.META.get('HTTP_X_FORWARDED_FOR')

        if redirected:
            return redirected.split(',')[0]
        else:
            return request.META.get('REMOTE_ADDR')

    def save_form(self, form):
        """Сохранение отзыва к товару"""
        if form.is_valid():
            form = form.cleaned_data
            Review.objects.update_or_create(
                name=form['name'],
                email=form['email'],
                text=form['text'],
                ipaddress=self.get_user_ip(self.request),
                product=form["product"],
                grade=form['grade'],
            )
            

        else:
            pass


class FavoritesActions:

    @staticmethod
    def add_product_from_favorites(user_id, product_id):
        """Добавление продукта к избранному для авторизованного пользователя"""
        user = User.objects.get(id=user_id)
        product_id = Card_Product.objects.get(id=product_id)
        try:
            favorite_item = Favorites.objects.create(user=user, products=product_id)
            favorite_item.save()
        except IntegrityError as Ie:
            pass

    @staticmethod
    def remove_product_from_favorites(user_id, product_id):
        """Удаление продукта из избранного для авторизованного пользователя"""
        user = User.objects.get(id=user_id)
        product_id = Card_Product.objects.get(id=product_id)
        favorite_item = Favorites.objects.get(user=user, products=product_id)
        favorite_item.delete()


class CartActions:

    @staticmethod
    def add_to_card(user_id, product_id):
        """Добавление продукта в корзину"""
        user = User.objects.get(id=user_id)
        product_id = Card_Product.objects.get(id=product_id)
        try:
            selected_product = Cart.objects.create(user=user, product=product_id)
            selected_product.save()
        except IntegrityError as Ie:
            update_concrete_item = Cart.objects.get(user=user, product=product_id)
            update_concrete_item.total += 1
            update_concrete_item.save()

    @staticmethod
    def pop_from_card(user_id, product_id):
        """Вычитание продукта из корзины. Если количество продукта 0, то продукт удаляется из корзины"""
        user = User.objects.get(id=user_id)
        product_id = Card_Product.objects.get(id=product_id)
        update_concrete_item = Cart.objects.get(user=user, product=product_id)
        update_concrete_item.total -= 1
        if update_concrete_item.total <= 0:
            update_concrete_item.delete()
        else:
            update_concrete_item.save()

    @staticmethod
    def del_from_cart(user_id, product_id):
        """Удаление продукта из корзины пользователя"""
        user = User.objects.get(id=user_id)
        product_id = Card_Product.objects.get(id=product_id)
        selected_item = Cart.objects.get(user=user, product=product_id)
        selected_item.delete()
        


class OrderActions:

    def get_products_for_pay(self) -> [object, bool]:
        """Получить перечень всех продуктов добавленных в корзину"""
        try:
            obj = Cart.objects.filter(user=self.request.user.id).select_related('product')
            return obj
        except Exception as error:
            return False

    def get_total_price(self) -> [object, bool]:
        """Получение итоговой стоимости всех товаров в корзине пользователя"""
        try:
            obj = Cart.total_price(user_pk=self.request.user.id)
            return obj
        except Exception as error:
            return False

    def get_default_delivery(self) -> [object, bool]:
        """Получение сохраненного по умолчанию адреса доставки"""
        try:
            obj = DefaultDelivery.objects.get(user=self.request.user.id)
            return obj
        except ObjectDoesNotExist as e:
            self.select_first_saved_address_on_default()
            return False

    def select_first_saved_address_on_default(self):
        """Установка по умолчанию первого сохраненного адреса доставки, если таковой имеется"""
        try:
            default_address = Delivery.objects.filter(user=self.request.user.id)
            user = User.objects.get(id=self.request.user.id)
            default = Delivery.objects.get(id=default_address[0].id)
            new_default_address = DefaultDelivery.objects.create(user=user, default=default)
            new_default_address.save()
        except IndexError:
            return False

    def get_addresses(self) -> [object, bool]:
        """Получение всех сохраненных адресов для выбора в качестве основного"""
        try:
            obj = Delivery.objects.filter(user=self.request.user.id).values('id', 'address_header')
            return obj
        except Exception as e:
            return False

    def select_new_address_for_delivery(self):
        """Пользователь выбирает адрес для доставки и заполняет таблицу заказа данными"""
        try:
            user = User.objects.get(id=self.request.user.id)
            old_default_address = DefaultDelivery.objects.get(user=user)
            old_default_address.delete()

            address = Delivery.objects.get(id=self.request.POST['address_form'])
            new_default_address = DefaultDelivery.objects.create(user=user, default=address)
            new_default_address.save()

        except Exception as e:
            pass


class BuyActions:

    @staticmethod
    def get_data_about_user(user_instance) -> tuple:
        """Получение данных о пользователе, которые понадобятся при оформлении заказа"""
        default_delivery_instance = DefaultDelivery.objects.get(user=user_instance)
        user_info = (
            default_delivery_instance.default.name_first,
            default_delivery_instance.default.name_last,
            default_delivery_instance.default.phone,
            default_delivery_instance.default.address,
            default_delivery_instance.default.comment,
        )
        return user_info

    @staticmethod
    def create_buy_product_instances(user_instance) -> tuple:
        """Сохранение в базу данных количество приобретаемого товара"""
        cart_instance = Cart.objects.filter(user=user_instance)
        what_products_were_purchased = list()
        for cart in cart_instance:
            product_instance = cart.product
            total_instance = cart.total
            buy_instance = BuyProduct.objects.create(product_for_buy=product_instance, total=total_instance)
            what_products_were_purchased.append(buy_instance.id)
        return tuple(what_products_were_purchased)

    @staticmethod
    def get_total_price(user_instance) -> float:
        """Получение итоговой стоимости"""
        total_price = Cart.total_price(user_pk=user_instance)
        return round(total_price, 2)

    @staticmethod
    def another_create_order(user, info, total):
        """Создание заказа"""
        cart = Cart.objects.filter(user=user.id)
        cards_ids = [i.id for i in cart]
        cards_obj = Card_Product.objects.filter(id__in=cards_ids)

        order = Order.objects.create(
            user=user,
            total=total,
            name_first=info[0],
            name_last=info[1],
            phone=info[2],
            address=info[3],
            message=info[4]
        )
        order.cards.add(*cards_obj)

    @staticmethod
    def deleting_selected_products_in_cart(user_instance):
        """Удаление всех товаров из корзины пользователя"""
        selected_item = Cart.objects.filter(user=user_instance)
        selected_item.delete()
        

    def pay_for_the_goods(self, user_id):
        """Запуск цепочки оплаты"""
        user_instance = User.objects.get(id=user_id)
        user_info = self.get_data_about_user(user_instance)
        total = self.get_total_price(user_instance)
        self.another_create_order(user_instance, user_info,  total)
        # Тут должна быть оплата
        self.deleting_selected_products_in_cart(user_instance)
