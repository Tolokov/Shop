from django.shortcuts import render

def ex404(request, exception):
    context = {'errorMessage': 'Новость не существует!'}
    if exception:
        pass
    request = render(request, 'exception/404.html', status=404, context=context)
    return request


def ex500(request, *exception):
    context = {'errorMessage': 'Произошла внутренняя ошибка сервера!'}
    if exception:
        pass
    request = render(request, 'exception/500.html', status=500, context=context)
    return request
