from django.forms import CharField, EmailField, BooleanField, Form, ModelChoiceField, Textarea
from .models import Delivery, User


class AddNewAddressDeliveryForm(Form):
    user = ModelChoiceField(queryset=User.objects.all())

    address_header = CharField(max_length=500)
    email = EmailField(max_length=254)
    notification_on_email = BooleanField()

    name_first = CharField(max_length=500)
    name_last = CharField(max_length=500)

    address = CharField(max_length=500)
    country = CharField(max_length=500)
    state = CharField(max_length=500)

    zip = CharField(max_length=10)
    phone = CharField(max_length=20)
    sub_phone = CharField(max_length=20)
    fax = CharField(max_length=20)
    comment = CharField()


class ContactForm(Form):
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
