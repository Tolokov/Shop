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
    name = CharField()
    email = CharField()
    text = CharField(widget=Textarea)


