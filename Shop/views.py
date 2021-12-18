from django.shortcuts import render
from django.views.generic import View

from .models import News


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
        return render(request, 'pages/index.html')

class BlogView(View):
    def get(self, request):
        posts = News.objects.filter(draft=False)
        return render(request, 'pages/blog.html', {'posts': posts})

class SinglePostVies(View):
    def get(self, request, post_id):
        single_post = News.objects.get(id=post_id)
        return render(request, 'pages/blog-single.html', {'single_post': single_post})


