from django.shortcuts import render
from django.views.generic import View

from .models import News, Cart_Product


# def ex404(request, exception):
#     context = {}
#     context['page_title'] = '404'
#     response = render(request, 'exception/404.html', status=404)
#     response.status_code = 404
#     return response

def ex404(request, exception):
    return render(request, 'exception/404.html', status=404)

class HomeView(View):
    def get(self, request):
        products = Cart_Product.objects.filter(availability=False)
        return render(request, 'pages/index.html', {'products': products})

class BlogView(View):
    def get(self, request):
        posts = News.objects.filter(draft=False)
        return render(request, 'pages/blog.html', {'posts': posts})

class SinglePostVies(View):
    def get(self, request, post_id):
        single_post = News.objects.get(id=post_id)
        return render(request, 'pages/blog-single.html', {'single_post': single_post})


# /////////////////////////////

class CartView(View):
    def get(self, request):
        return render(request, 'pages/cart.html', {})

class CheckoutView(View):
    def get(self, request):
        return render(request, 'pages/checkout.html', {})

class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact-us.html', {})

class ShopView(View):
    def get(self, request):
        return render(request, 'pages/shop.html', {})

class Product_detailView(View):
    def get(self, request):
        return render(request, 'pages/product-detail.html', {})


class FavoritesView(View):
    def get(self, request):
        return render(request, 'pages/product-detail.html', {})








