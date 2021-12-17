from django.shortcuts import render
from django.views.generic import View

# def ex404(request, exception):
#     context = {}
#     context['page_title'] = '404'
#     response = render(request, 'exception/404.html', status=404)
#     response.status_code = 404
#     return response

def ex404(request, exception):
    return render(request, 'exception/404.html', status=404)

class PostView(View):
    def get(self, request):
        return render(request, 'pages/login.html')


