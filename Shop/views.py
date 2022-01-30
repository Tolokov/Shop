from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.db.models import Avg
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.http import JsonResponse

from Interactive.models import Delivery
from Shop.models import Card_Product, Category, Review, ProductImage, Favorites, User, Cart, DefaultDelivery
from Shop.forms import ReviewForm
from Shop.utils import DataMixin

from Shop.service import JsonHandler


class HomeListView(DataMixin, ListView):
    """Главная страница"""
    template_name = 'pages/index.html'
    queryset = Card_Product.objects.filter(availability=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Формирование отображаемых на главной странице карточек разложенных по категориям и рекомендациям"""
        context = super().get_context_data(**kwargs)
        del context['title']
        del context['shop_selected']
        context['title'] = 'Главная страница'
        context['home_selected'] = 'active'

        recommended_items = self.get_recommended_queryset(self.queryset)
        context['recommended_item'] = recommended_items[0]
        context['recommended_next_items'] = recommended_items[1]

        context['categories'] = Category.objects.all().order_by('name').prefetch_related('card_product_set')
        return context


class ShopListView(DataMixin, ListView):
    """Страница каталога продуктов с фильтрацией"""
    template_name = 'pages/shop.html'
    queryset = Card_Product.objects.filter(availability=False).values('name', 'price', 'image', 'id', 'condition')


class JsonFilterProductView(DataMixin, ListView, JsonHandler):
    """Ajax фильтр"""
    queryset = Card_Product.objects.filter(availability=False)

    def get_queryset(self):
        """Формирование ответа"""
        queryset = self.handler()
        return queryset

    def get(self, request, *args, **kwargs):
        """Получение запроса к ajax и формирование json"""
        queryset = self.json_answer()
        return JsonResponse({"json_answer": queryset}, safe=False)


class ProductDetailView(FormView, DetailView):
    """Карточка продукта"""
    model = Card_Product
    template_name = 'pages/product-detail.html'
    context_object_name = 'product_detail'
    pk_url_kwarg = 'product_ID'
    form_class = ReviewForm
    queryset = Card_Product.objects.filter(availability=False).select_related('brand').prefetch_related('category')

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name

        context['form'] = ReviewForm()
        review_queryset = Review.objects.filter(product=self.object).select_related('grade')
        context['reviews'] = review_queryset
        context['count'] = review_queryset.__len__()

        if context['reviews']:
            avg = review_queryset.aggregate(Avg('grade__value'))['grade__value__avg']
            stars = round(avg)
            context['grade_on'] = range(stars)
            context['grade_off'] = range(5 - stars)
        else:
            context['avg_grade'] = False

        product_images_queryset = ProductImage.objects.filter(product=self.object)
        context['slider'] = self.paginator_optimization(product_images_queryset)
        return context

    @staticmethod
    def paginator_optimization(queryset, per_page=3, max_pages=5):
        """Paginator optimization (9 SQL queries --> 6 SQL queries)"""
        list_objects = list(queryset[:per_page * max_pages])
        paginator_object = paginator.Paginator(list_objects, per_page=per_page)
        return paginator_object

    def get_ip(self, request):
        redirected = request.META.get('HTTP_X_FORWARDED_FOR')
        return redirected.split(',')[0] if redirected else request.META.get('REMOTE_ADDR')

    def post(self, request, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form = form.cleaned_data
            Review.objects.update_or_create(
                name=form['name'],
                email=form['email'],
                text=form['text'],
                ipaddress=self.get_ip(self.request),
                product=form["product"],
                grade=form['grade'],
            )
        else:
            print('проверка не прошла')
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class FavoritesView(ListView):
    """Отображение страницы со всеми сохраненными адресами доставки"""
    model = Favorites
    template_name = 'pages/favorites.html'
    context_object_name = 'favorites_items'

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user.id).select_related('products')


class AddFavoritesView(FavoritesView):
    """Добавление в избранное"""

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        try:
            favorite_item = Favorites.objects.create(user=user, products=product_id)
            favorite_item.save()
        except IntegrityError as Ie:
            print('Обнаружен дубликат!', {Ie})
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class DeleteFavoritesView(FavoritesView):
    """Удаление продукта из избранного"""

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        favorite_item = Favorites.objects.get(user=user, products=product_id)
        favorite_item.delete()
        return redirect(reverse_lazy('favorites'), permanent=True)


class CartListView(ListView):
    """Отображение всех продуктов добавленных в корзину"""
    model = Cart
    template_name = 'pages/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user.id).select_related('product')


class AddCart(CartListView):
    """Добавление единицы товара в корзину"""

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        try:
            selected_product = Cart.objects.create(user=user, product=product_id, total=1)
            selected_product.save()
        except IntegrityError as Ie:
            print('Обнаружен дубликат!', {Ie})
            update_product = Cart.objects.get(user=user, product=product_id)
            update_product.total += 1
            update_product.save()
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class PopCart(CartListView):
    """Вычитание продукта из корзины товаров. Если количество продукта 0, то продукт удаляется из корзины"""

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        update_product = Cart.objects.get(user=user, product=product_id)
        update_product.total -= 1
        if update_product.total <= 0:
            update_product.delete()
        else:
            update_product.save()
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class DeleteCartProduct(CartListView):
    """Удаление продукта из корзины товаров"""

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        selected_item = Cart.objects.get(user=user, product=product_id)
        selected_item.delete()
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class OrderListView(LoginRequiredMixin, ListView):
    """Формирование заказа"""
    model = Cart
    template_name = 'pages/order.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id

        context['products_for_pay'] = Cart.objects.filter(user=user_id).select_related('product')
        context['total_price'] = Cart.total_price(user_pk=user_id)

        try:
            context['user_delivery'] = DefaultDelivery.objects.get(user=user_id)

        except Exception as e:
            print('Ошибка при оформлении адреса доставки:', e)
            default_address = Delivery.objects.filter(user=user_id)
            new_default_address = DefaultDelivery.objects.create(
                user=User.objects.get(id=user_id),
                default=Delivery.objects.get(id=default_address[0].id))
            new_default_address.save()

        try:
            context['addresses'] = Delivery.objects.filter(user=user_id).values('id', 'address_header')
        except Exception as e:
            print('Оформление заказа с пустой корзиной', e)

        return context

    def post(self, request, **kwargs):
        user_id = self.request.user.id
        try:
            old_default_address = DefaultDelivery.objects.get(user=User.objects.get(id=user_id))
            old_default_address.delete()
            new_default_address = DefaultDelivery.objects.create(
                user=User.objects.get(id=user_id),
                default=Delivery.objects.get(id=self.request.POST['address_form'])
            )
            new_default_address.save()
        except Exception as e:
            print('Ошибка заполнения формы адреса, данными', e)

        return redirect(reverse_lazy('order'), permanent=True)
