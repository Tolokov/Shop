from django.forms import TextInput, Form, ModelForm, CharField, Textarea, EmailField, IntegerField
from Shop.models import Delivery


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


class ContactForm(Form):
    """Форма обращения в техническую поддержку через smtp.gmail"""
    required = {"required": "required"}

    name_attrs = {
        "class": "form-control",
        "type": "text",
        "name": "name",
        "placeholder": "Name",
    } | required

    email_attrs = {
        "class": "form-group col-md-6 form-control",
        "type": "email",
        "name": "email",
        "placeholder": "Email",
    } | required

    text_attrs = {
        "class": "form-group col-md-18 form-control",
        "name": "message",
        "id": "message",
        "rows": "8",
    } | required

    name = CharField()
    name.widget.attrs.update(name_attrs)
    email = EmailField()
    email.widget.attrs.update(email_attrs)
    text = CharField(widget=Textarea(attrs=text_attrs))


class ReviewForm(Form):
    """Добавление отзыва к карточке продукта"""
    required = {
        "required": "required",
        "class": "form-group col-md-6 form-control",
    }
    name_attrs = {
        "type": "text",
        "placeholder": "Your Name",
        "name": "name",
    } | required

    email_attrs = {
        "type": "email",
        "placeholder": "Email Address",
    } | required

    text_attrs = {
        "name": "text",
        "placeholder": "Text",
    } | required

    name = CharField(max_length=149)
    name.widget.attrs.update(name_attrs)
    email = EmailField()
    email.widget.attrs.update(email_attrs)
    text = CharField(widget=Textarea())
    text.widget.attrs.update(text_attrs)
    grade = IntegerField(max_value=10, min_value=0)



