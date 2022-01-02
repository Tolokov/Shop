from django.shortcuts import render, redirect, reverse
from django.views.generic import View, ListView, DetailView, FormView, UpdateView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import News, Card_Product, Category, Comment, Review
from .forms import *
from django.conf import settings
from django.core.mail import send_mail


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
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(draft=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новостной блог'
        context['blog_selected'] = 'active'
        context['headline'] = ('Latest From our Blog', 'Читать дальше...')
        return context


class BlogDetailView(FormView, DetailView):
    model = News
    template_name = 'pages/blog-single.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'single_post'
    queryset = News.objects.filter(draft=False)
    form_class = AddCommentForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.object)
        context['count'] = context['comments'].count()
        context['responses'] = 'Отзывов'
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(BlogDetailView, self).form_valid(form)

    def post(self, request, pk, *args, **kwargs):
        form = AddCommentForm(request.POST)
        news = News.objects.get(id=pk)
        if form.is_valid():
            form = form.cleaned_data
            comment = Comment(
                text=form['text'],
                parent=form['parent'],
                news=news,
                creator=form['creator'],
            )
            comment.save()

        return redirect(news.get_absolute_url())


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


class ShopListView(ListView):
    model = Card_Product
    template_name = 'pages/shop.html'
    context_object_name = 'products'
    queryset = Card_Product.objects.filter(availability=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['shop_selected'] = 'active'
        return context


class ProductDetailView(FormView, DetailView):
    model = Card_Product
    template_name = 'pages/product-detail.html'
    context_object_name = 'product_detail'
    pk_url_kwarg = 'product_ID'
    queryset = Card_Product.objects.filter(availability=False)
    form_class = ReviewForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['reviews'] = Review.objects.filter(product=self.object)
        context['count'] = context['reviews'].count()
        return context

    def post(self, request, pk, *args, **kwargs):
        form = ReviewForm(request.POST)
        product = Card_Product.objects.get(id=pk)
        if form.is_valid():
            form = form.cleaned_data
            # print([type(i) for i in form])
            review = Review(
                name=form['name'],ipaddress='127.0.0.1',email=form['email'],
                text=form['text'],product=product,g=int(form['grade']),)
            review.save()
        return redirect(product.get_absolute_url())


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
            'New York USA',
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
        form = form.cleaned_data
        print(form)
        send_mail(form['name'],
                  ('Отправитель: {} \nТекст сообщеня:\n{}').format(form['email'], form['text']),
                  settings.EMAIL_HOST_USER,
                  [settings.EMAIL_HOST_USER],
                  fail_silently=False)

        return super(ContactFormView, self).form_valid(form)


class DeliveryFormView(FormView):
    template_name = 'pages/delivery.html'
    form_class = AddNewAddressDeliveryForm

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        print(form.cleaned_data)
        form.save(self)
        return super(DeliveryFormView, self).form_valid(form)


class CartView(View):
    def get(self, request):
        return render(request, 'pages/cart.html', {})


class FavoritesView(View):
    def get(self, request):
        return render(request, 'pages/product-detail.html', {})
