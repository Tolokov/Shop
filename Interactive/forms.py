from django.forms import Form, CharField, Textarea, EmailField, ModelForm, TextInput, ImageField, FileInput, EmailInput
from django.core.exceptions import ValidationError
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from Interactive.models import Customer, Delivery, Mail


class MailForm(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Mail
        fields = ('email', 'captcha')
        widgets = {'email': TextInput(attrs={'placeholder': 'Подписаться'})}
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
    # <input type="hidden" value="{{ user.id }}" name="user">

    class Meta:
        required = {"required": "required"}
        pattern = {"class": "form-group", "type": "text"}

        model = Delivery
        fields = '__all__'
        widgets = {
            'user': TextInput(attrs={"placeholder": "user", "type": "hidden"}),
            'address_header': TextInput(attrs={"placeholder": "Display title on delivery"} | pattern | required),
            'name_first': TextInput(attrs={"placeholder": "First Name"} | pattern | required),
            'name_last': TextInput(attrs={"placeholder": "Last Name"} | pattern | required),
            'address': TextInput(attrs={"placeholder": "Delivery address"} | pattern | required),
            'country': TextInput(attrs={"placeholder": "The country"} | pattern | required),
            'state': TextInput(attrs={"placeholder": "Region"} | pattern | required),
            'phone': TextInput(attrs={"placeholder": "Phone number"} | pattern | required),
            'sub_phone': TextInput(attrs={"placeholder": "Additional phone number"} | pattern),
            'zip': TextInput(attrs={"placeholder": "Postcode"} | pattern),
            'comment': Textarea(attrs={"placeholder": "Additional shipping comment"} | pattern),
            'email': EmailInput(attrs={"placeholder": "Email"} | pattern | required),
        }

    def clean(self):
        data = self.cleaned_data
        if Delivery.objects.filter(user=data['user'],
                                   address_header=data['address_header']).exists():
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
