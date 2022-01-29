from django.shortcuts import render

from logging import getLogger

logger = getLogger(__name__)


def ex404(request, exception):
    context = {'errorMessage': 'Мы не смогли найти эту страницу!'}
    logger.info('404 ')
    if isinstance(exception, int):
        context['errorMessage'] = 'Новость не существует'
    request = render(request, 'exception/404.html', status=404, context=context)
    return request


