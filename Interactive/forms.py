from django.forms import Form, CharField, Textarea, EmailField


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


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
