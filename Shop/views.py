from django.shortcuts import render
from django.views.generic import View

from .models import News, Card_Product, Category


def ex404(request, exception):
    context = {'errorMessage': 'We Couldn’t Find this Page'}
    print(exception)
    if isinstance(exception, int):
        context['errorMessage'] = 'Новость не существует'
    request = render(request, 'exception/404.html', status=404, context=context)
    return request


class HomeView(View):
    def get(self, request):
        products = Card_Product.objects.filter(availability=False)
        return render(request, 'pages/index.html', {
            'products': products,
        })


class ProductDetailView(View):
    def get(self, request, product_public_ID):
        product_detail = Card_Product.objects.get(product_public_ID=product_public_ID)
        return render(request, 'pages/product-detail.html', {'product_detail': product_detail})


class BlogListView(View):
    def get(self, request):
        posts = News.objects.filter(draft=False)
        return render(request, 'pages/blog.html', {'posts': posts})


class SinglePostVies(View):
    def get(self, request, post_id):
        single_post = News.objects.get(id=post_id)
        if single_post.draft:
            return ex404(request, exception=post_id)
        else:
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


class FavoritesView(View):
    def get(self, request):
        return render(request, 'pages/product-detail.html', {})
