from django.shortcuts import render
from django.views.generic import View


class PostView(View):
    def get(self, request):
        return render(request, 'pages/index.html')





