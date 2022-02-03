from django.core.mail import send_mail
from e_shopper.settings import EMAIL_HOST_USER, EMAIL_HOST_USER

from Interactive.models import Mail
from Interactive.forms import MailForm

from logging import getLogger

logger = getLogger(__name__)

try:
    def send_mail_to_support(form_data):
        """Формирование письма"""
        message = f"Отправитель: {form_data['email']} \nТекст сообщеня:\n{form_data['text']}"
        send_mail(form_data['name'], message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False)
        logger.info('Отправлено электронное письмо через страницу обратной связи')
except Exception as error:
    logger.warning(f'Непредвиденная ошибка при отправке письма\n {error}')


def save_mail_or_error(request):
    form = MailForm(request.POST)
    try:
        if form.is_valid:
            email = form.data['email']
            print()
            if Mail.objects.filter(email=email).exists():
                raise NameError('Почтовый адрес уже сохранен')
            form.save()
    except NameError as err:
        logger.info(err)

    except ValueError as err:
        logger.info(err)
