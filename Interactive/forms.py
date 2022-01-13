from django.forms import Form, CharField, Textarea, EmailField, ModelForm, TextInput, ImageField, FileInput
from Interactive.models import Customer, Delivery


class ContactForm(Form):
    """Форма обращения в техническую поддержку через smtp.gmail"""
    name = CharField()
    email = EmailField()
    text = CharField(widget=Textarea())

    name_attrs = {
        "class": "form-control",
        "type": "text",
        "name": "name",
        "placeholder": "Name",
        "required": "required"
    }

    email_attrs = {
        "class": "form-group col-md-6 form-control",
        "type": "email",
        "name": "email",
        "placeholder": "Email",
        "required": "required"
    }

    text_attrs = {
        "class": "form-group col-md-18 form-control",
        "type": "message",
        "name": "message",
        "id": "message",
        "placeholder": "Message",
        "rows": "8",
        "required": "required"
    }

    name.widget.attrs.update(name_attrs)
    email.widget.attrs.update(email_attrs)
    text.widget.attrs.update(text_attrs)


class CustomerForm(ModelForm):
    avatar = ImageField(label='Установить новое изображение:', required=False, widget=FileInput, )

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class AddNewAddressDeliveryForm(ModelForm):
    """Форма добавления адреса для доставки"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].empty_label = 'Это поле должно быть выбрано автоматически'

    class Meta:
        model = Delivery
        fields = '__all__'
        widgets = {
            'address_header': TextInput(attrs={"placeholder": "header"}),
            'name_first': TextInput(attrs={"placeholder": "name_first"}),
            'name_last': TextInput(attrs={"placeholder": "name_last"}),
            'address': TextInput(attrs={"placeholder": "address"}),
            'country': TextInput(attrs={"placeholder": "country"}),
            'state': TextInput(attrs={"placeholder": "state"}),
            'phone': TextInput(attrs={"placeholder": "phone"}),
            'sub_phone': TextInput(attrs={"placeholder": "sub_phone"}),
            'zip': TextInput(attrs={"placeholder": "zip"}),
        }
