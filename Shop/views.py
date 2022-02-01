from django.views.generic import ListView, DetailView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse

from Shop.service import JsonHandler, ProductDetailMixin, FavoritesActions, CartActions, OrderActions, BuyActions
from Shop.models import Card_Product, Category, ProductImage, Favorites, Cart
from Shop.forms import ReviewForm
from Shop.utils import MixinForMainPages


class HomeListView(MixinForMainPages, ListView):
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
        self.get_recommended_queryset(self.queryset, context)
        context['categories'] = Category.objects.all().order_by('name').prefetch_related('card_product_set')
        return context


class ShopListView(MixinForMainPages, ListView):
    """Страница каталога продуктов с фильтрацией"""
    template_name = 'pages/shop.html'
    queryset = Card_Product.objects.filter(availability=False).values('name', 'price', 'image', 'id', 'condition')[:18]


class JsonFilterProductView(MixinForMainPages, ListView, JsonHandler):
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


class ProductDetailView(FormView, DetailView, ProductDetailMixin):
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
        self.get_review_queryset(context)
        context['slider'] = self.paginator_optimization(ProductImage.objects.filter(product=self.object))
        return context

    def post(self, request, **kwargs):
        self.save_form(ReviewForm(request.POST))
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class FavoritesView(ListView):
    """Отображение страницы со всеми сохраненными адресами доставки"""
    model = Favorites
    template_name = 'pages/favorites.html'
    context_object_name = 'favorites_items'

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user.id).select_related('products')


class AddFavoritesView(FavoritesView, FavoritesActions):
    """Добавление в избранное"""

    def post(self, request, **kwargs):
        self.add_product_from_favorites(request.user.id, kwargs['product_id'])
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class DeleteFavoritesView(FavoritesView, FavoritesActions):
    """Удаление продукта из избранного"""

    def post(self, request, **kwargs):
        self.remove_product_from_favorites(request.user.id, kwargs['product_id'])
        return redirect(reverse_lazy('favorites'), permanent=True)


class CartListView(ListView):
    """Отображение всех продуктов добавленных в корзину"""
    model = Cart
    template_name = 'pages/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user.id).select_related('product')


class AddCart(CartListView, CartActions):
    """Добавление единицы товара в корзину"""

    def post(self, request, **kwargs):
        self.add_to_card(request.user.id, kwargs['product_id'])
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class PopCart(CartListView, CartActions):
    """Уменьшение количества одинаковых продуктов в корзину."""

    def post(self, request, **kwargs):
        self.pop_from_card(request.user.id, kwargs['product_id'])
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class DeleteCartProduct(CartListView, CartActions):
    """Удаление продукта из корзины товаров"""

    def post(self, request, **kwargs):
        self.del_from_cart(request.user.id, kwargs['product_id'])
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class OrderListView(LoginRequiredMixin, ListView, OrderActions):
    """Формирование заказа"""
    model = Cart
    template_name = 'pages/order.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_for_pay'] = self.get_products_for_pay()
        context['total_price'] = self.get_total_price()
        context['user_delivery'] = self.get_default_delivery()
        context['addresses'] = self.get_addresses()
        return context

    def post(self, request, **kwargs):
        self.select_new_address_for_delivery()
        return redirect(reverse_lazy('order'), permanent=True)


class BuyView(View, BuyActions):
    def post(self, request, **kwargs):
        self.pay_for_the_goods(self.request.user.id)
        return redirect(reverse_lazy('order'), permanent=True)



