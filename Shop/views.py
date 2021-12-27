from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, FormView
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


class ShopListView(HomeListView):
    template_name = 'pages/shop.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['shop_selected'] = 'active'
        context.pop('home_selected')
        return context


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


class ContactFormView(FormView):
    template_name = 'pages/contact-us.html'
    form_class = ContactForm
    success_url = '/contact/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CONTACT US'
        context['contact_selected'] = 'active'
        contact_info = (
            'E-Shopper Inc.',
            '935 W. Webster Ave New Streets Chicago, IL 60614, NY',
            'Newyork USA',
            'Mobile: +2346 17 38 93',
            'Fax: 1-714-252-0026',
            'Email: info@e-shopper.com',
        )
        context['contact_info'] = contact_info

        context['headline'] = (
            'Contact US', 'get in touch', 'contact info', 'SOCIAL NETWORKING'
        )
        context['social_networking'] = (
            ('fa-facebook', '#'),
            ('fa-twitter', '#'),
            ('fa-google-plus', '#'),
            ('fa-youtube', '#')
        )
        return context

    def form_valid(self, form):
        self.send_masage(form.cleaned_data)
        return super(ContactFormView, self).form_valid(form)

    def send_masage(self, void_valid):
        print(void_valid)
        pass


# /////////////////////////////

class DeliveryView(View):
    def get(self, request):
        form = AddNewAddressDeliveryForm()
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


class CartView(View):
    def get(self, request):
        return render(request, 'pages/cart.html', {})


class FavoritesView(View):
    def get(self, request):
        return render(request, 'pages/product-detail.html', {})
