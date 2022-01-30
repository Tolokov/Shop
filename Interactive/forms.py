from django.forms import Form, CharField, Textarea, EmailField, ModelForm, TextInput, ImageField, FileInput, EmailInput
from django.core.exceptions import ValidationError
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from Interactive.models import Customer, Delivery, Mail

from logging import getLogger

logger = getLogger(__name__)


class MailForm(ModelForm):
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(MailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Подписаться'

    class Meta:
        model = Mail
        fields = ('email', 'captcha')
        widgets = {'email': EmailInput()}
        labels = {'email': ''}


class CustomerForm(ModelForm):
    avatar = ImageField(label='Установить новое изображение:', required=False, widget=FileInput)

    class Meta:
        pattern = TextInput(attrs={"class": "form-control", "type": "text"})

        model = Customer
        fields = '__all__'
        exclude = ['user']
        widgets = {'first_name': pattern, 'last_name': pattern, 'phone': pattern, 'email': pattern, 'avatar': pattern}


class AddNewAddressDeliveryForm(ModelForm):
    """Форма добавления адреса для доставки со скрытым полем пользователя"""

    class Meta:
        required = {"required": "required"}
        pattern = {"class": "form-group", "type": "text"}

        model = Delivery
        fields = '__all__'
        widgets = {
            'user': TextInput(attrs={"placeholder": "user", "type": "hidden"}),
            'address_header': TextInput(attrs={"placeholder": "Название сохраняемого адреса"} | pattern | required),
            'name_first': TextInput(attrs={"placeholder": "Фамилия"} | pattern | required),
            'name_last': TextInput(attrs={"placeholder": "Имя"} | pattern | required),
            'address': TextInput(attrs={"placeholder": "Город, улица, дом, квартира"} | pattern | required),
            'country': TextInput(attrs={"placeholder": "Страна"} | pattern | required),
            'state': TextInput(attrs={"placeholder": "Регион"} | pattern | required),
            'phone': TextInput(attrs={"placeholder": "Номер телефона"} | pattern | required),
            'sub_phone': TextInput(attrs={"placeholder": "Номер телефона дополнительно"} | pattern),
            'zip': TextInput(attrs={"placeholder": "Индекс"} | pattern),
            'comment': Textarea(attrs={"placeholder": "Комментарий к адресу"} | pattern),
            'email': EmailInput(attrs={"placeholder": "Электронная почта"} | pattern | required),
        }

    def clean(self):
        data = self.cleaned_data
        if Delivery.objects.filter(user=data['user'],
                                   address_header=data['address_header']).exists():
            logger.debug(f'Пользователь попытался сохранить уже существующий адрес доставки: user_id:{data["user"]}')
            raise ValidationError(f'Адресс доставки с таким названием уже сохранен')
        return data


class ContactForm(Form):
    """Форма обращения в техническую поддержку через smtp.gmail"""

    name = CharField(widget=TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "name": "name",
        "placeholder": "Name",
        "required": "required"
    }))

    email = EmailField(widget=TextInput(attrs={
        "class": "form-group col-md-6 form-control",
        "type": "email",
        "name": "email",
        "placeholder": "Email",
        "required": "required"
    }))

    text = CharField(widget=Textarea(attrs={
        "class": "form-group col-md-18 form-control",
        "type": "message",
        "name": "message",
        "id": "message",
        "placeholder": "Message",
        "rows": "8",
        "required": "required"
    }))
