from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import News, Card_Product, Category
from .forms import *


def ex404(request, exception):
    context = {'errorMessage': 'We Couldn’t Find this Page'}
    print(exception)
    if isinstance(exception, int):
        context['errorMessage'] = 'Новость не существует'
    request = render(request, 'exception/404.html', status=404, context=context)
    return request


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class BlogListView(ListView):
    model = News
    template_name = 'pages/blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return News.objects.filter(draft=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новостной блог'
        context['blog_selected'] = 'active'
        return context


class BlogDetailView(DetailView):
    model = News
    template_name = 'pages/blog-single.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'single_post'

    def get_queryset(self):
        return News.objects.filter(draft=False)


class HomeListView(ListView):
    model = Card_Product
    template_name = 'pages/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['home_selected'] = 'active'
        return context

    def get_queryset(self):
        return Card_Product.objects.filter(availability=False)


class ProductDetailView(DetailView):
    model = Card_Product
    template_name = 'pages/product-detail.html'
    context_object_name = 'product_detail'
    pk_url_kwarg = 'product_ID'
    queryset = Card_Product.objects.filter(availability=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class DeliveryView(View):
    def get(self, request):
        form = AddNewAddressDeliveryForm()
        print('TUT ----------->', dir(form))
        return render(request, 'pages/delivery.html', {'form': form})

    def post(self, request):
        form = AddNewAddressDeliveryForm(request.POST)
        if form.is_valid():
            try:
                Delivery.objects.create(**form.cleaned_data)
                return redirect('/')
            except:
                form.add_error(None, 'Ошибка добавления адреса')
        else:
            form = AddNewAddressDeliveryForm()
        return render(request, 'pages/delivery.html', {'form': form})


# /////////////////////////////

class CartView(View):
    def get(self, request):
        return render(request, 'pages/cart.html', {})


class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact-us.html', {})


class ShopView(View):
    def get(self, request):
        return render(request, 'pages/shop.html', {})


class FavoritesView(View):
    def get(self, request):
        return render(request, 'pages/product-detail.html', {})
