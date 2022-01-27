from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core import serializers
from django.db.models import Count, Q, Avg
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.http import JsonResponse

from json import loads

from Shop.models import Card_Product, Category, Review, ProductImage, Favorites, User, Cart, DefaultDelivery
from Shop.forms import ReviewForm
from Shop.utils import DataMixin

from Interactive.models import Delivery


class HomeListView(DataMixin, ListView):
    """Главная страница"""
    template_name = 'pages/index.html'
    queryset = Card_Product.objects.filter(availability=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        del context['title']
        del context['shop_selected']
        context['title'] = 'Главная страница'
        context['home_selected'] = 'active'

        recommended_q = self.queryset.annotate(cnt=Count('review')).order_by('-cnt')
        recommended_q = self.cut_queryset(recommended_q.values('name', 'price', 'image', 'id', 'condition'))
        context['recommended_item'] = recommended_q[0]
        context['recommended_next_items'] = recommended_q[1:4]

        context['categories'] = Category.objects.all().order_by('name').prefetch_related('card_product_set')
        return context

    @staticmethod
    def cut_queryset(queryset, step=3) -> list:
        """ [[img,img,img.], [...], ...] """
        result = list()
        for i in range(0, len(queryset), step):
            result.append(queryset[i:i + step])
        return result


class ShopListView(DataMixin, ListView):
    """Страница с фильтрацией"""
    template_name = 'pages/shop.html'
    queryset = Card_Product.objects.filter(availability=False)


class JsonFilterProductView(DataMixin, ListView):

    def get_queryset(self):
        queryset = Card_Product.objects.filter(availability=False)
        if self.request.GET == {}:
            return queryset

        elif len(self.request.GET) == 2:
            queryset = queryset.filter(
                Q(category__in=self.request.GET.getlist("category")) &
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset

        else:
            queryset = queryset.filter(
                Q(category__in=self.request.GET.getlist("category")) |
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset

    def get(self, request, *args, **kwargs):
        queryset = serializers.serialize("json", self.get_queryset())
        queryset = loads(queryset)
        return JsonResponse({"json_answer": queryset}, safe=False)


class ProductDetailView(FormView, DetailView):
    """Подробности о продукте"""
    model = Card_Product
    template_name = 'pages/product-detail.html'
    context_object_name = 'product_detail'
    pk_url_kwarg = 'product_ID'
    form_class = ReviewForm

    def get_queryset(self):
        return Card_Product.objects.filter(availability=False).select_related('brand').prefetch_related('category')

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
        objects = list(queryset[:per_page * max_pages])
        paginator = Paginator(objects, per_page=per_page)
        return paginator

    def post(self, request, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
        else:
            print('проверка не прошла')

        # product = Card_Product.objects.get(id=kwargs['pk'])
        # grade = RatingGrade.objects.get(value=form['grade'])
        # if form.is_valid():
        #     print(product, grade)
            # form = form.cleaned_data
            # review = Review(
            #     name=form['name'], ipaddress='127.0.0.1', email=form['email'],
            #     text=form['text'], product=product, grade=grade,
            # )
            # review.save()
        # return redirect(product.get_absolute_url(), permanent=True)

        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class FavoritesView(ListView):
    model = Favorites
    template_name = 'pages/favorites.html'
    context_object_name = 'favorites_items'

    def get_queryset(self):
        return Favorites.objects.filter(user=self.request.user.id).select_related('products')


class AddFavoritesView(FavoritesView):

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        try:
            favorite_item = Favorites.objects.create(user=user, products=product_id)
            favorite_item.save()
        except IntegrityError as Ie:
            print('Обнаружен дубликат!', {Ie})
        return redirect(reverse_lazy('shop'), permanent=True)


class DeleteFavoritesView(FavoritesView):

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        favorite_item = Favorites.objects.get(user=user, products=product_id)
        favorite_item.delete()
        return redirect(reverse_lazy('favorites'), permanent=True)


class CartListView(ListView):
    model = Cart
    template_name = 'pages/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user.id).select_related('product')


class AddCart(CartListView):
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
    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        selected_item = Cart.objects.get(user=user, product=product_id)
        selected_item.delete()
        return redirect(request.META.get('HTTP_REFERER'), permanent=True)


class OrderListView(LoginRequiredMixin, ListView):
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
