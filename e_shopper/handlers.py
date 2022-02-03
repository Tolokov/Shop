from django.shortcuts import render

from logging import getLogger

logger = getLogger(__name__)


def ex404(request, exception):
    context = {'errorMessage': 'Новость не существует!'}
    logger.info('404 СТРАНИЦА НЕ НАЙДЕНА')
    if exception:
        logger.warning('Сработало исключение 404 при обращении к странице с сообщением:', exception)
    request = render(request, 'exception/404.html', status=404, context=context)
    return request


def ex500(request, *exception):
    context = {'errorMessage': 'Произошла внутренняя ошибка сервера!'}
    logger.info('500 ПРОИЗОШЛА ОШИБКА')
    if exception:
        logger.warning('Сработало исключение 500 при обращении к странице с сообщением:', exception)
    request = render(request, 'exception/500.html', status=500, context=context)
    return request
