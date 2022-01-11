from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.urls import reverse_lazy

from Shop.models import Card_Product, Category, Review, ProductImage, Favorites, User
from Shop.forms import ReviewForm, AddNewAddressDeliveryForm, Delivery
from Shop.utils import DataMixin


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

        recommended_queryset = self.queryset.annotate(cnt=Count('review')).order_by('-cnt')
        recommended_queryset = self.cut_queryset(recommended_queryset)
        context['recommended_item'] = recommended_queryset[0]
        context['recommended_next_items'] = recommended_queryset[1:4]

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


class FilterProductView(DataMixin, ListView):
    """Фильтр продуктов"""
    template_name = 'pages/shop.html'

    def get_queryset(self):

        if self.request.GET == {}:
            return Card_Product.objects.all()

        elif len(self.request.GET) == 2:
            queryset = Card_Product.objects.filter(
                Q(category__in=self.request.GET.getlist("category")) &
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset

        else:
            queryset = Card_Product.objects.filter(
                Q(category__in=self.request.GET.getlist("category")) |
                Q(brand__in=self.request.GET.getlist("brand"))).distinct()
            return queryset


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

        review_queryset = Review.objects.filter(product=self.object)
        context['reviews'] = review_queryset
        context['count'] = review_queryset.__len__()

        product_images_queryset = ProductImage.objects.filter(product=self.object)
        context['slider'] = self.paginator_optimizator(product_images_queryset)
        return context

    @staticmethod
    def paginator_optimizator(queryset, per_page=3, max_pages=5):
        """Paginator optimization (9 SQL queries --> 6 SQL queries)"""
        objects = list(queryset[:per_page * max_pages])
        paginator = Paginator(objects, per_page=per_page)
        return paginator

    def post(self, request, **kwargs):
        form = ReviewForm(request.POST)
        product = Card_Product.objects.get(id=kwargs['pk'])
        if form.is_valid():
            form = form.cleaned_data
            review = Review(
                name=form['name'], ipaddress='127.0.0.1', email=form['email'],
                text=form['text'], product=product, g=int(form['grade']),
            )
            review.save()
        return redirect(product.get_absolute_url())


class DeliveryFormView(LoginRequiredMixin, FormView):
    template_name = 'pages/delivery.html'
    form_class = AddNewAddressDeliveryForm
    success_url = '/delivery/'
    # Вместо 404 и перенаправления, пометка, доступ запрещен
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = Delivery.objects \
            .filter(user=self.request.user.id) \
            .values('id', 'user_id', 'address_header')
        return context

    def form_valid(self, form):
        form.save()
        print(form.cleaned_data)
        return super(DeliveryFormView, self).form_valid(form)

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
        except Exception as e:
            print('Обнаружен дубликат!', {e})
        return redirect(reverse_lazy('shop'))


class DeleteFavoritesView(FavoritesView):

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        product_id = Card_Product.objects.get(id=kwargs['product_id'])
        favorite_item = Favorites.objects.get(user=user, products=product_id)
        favorite_item.delete()
        return redirect(reverse_lazy('favorites'))


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pages/cart.html', {})
