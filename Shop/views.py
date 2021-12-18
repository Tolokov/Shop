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
        news = News.objects.all()
        return render(request, 'pages/blog.html', {'posts': news})

# class SinglePostVies(View):
#     def get(self, request):
#         posts = News.objects.all()
#         return render(request, 'pages/blog.html', {posts: 'posts'})


