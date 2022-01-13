from django.forms import Form, CharField, Textarea, EmailField, IntegerField


class ReviewForm(Form):
    """Добавление отзыва к карточке продукта"""
    name = CharField(max_length=149)
    email = EmailField()
    text = CharField(widget=Textarea())
    grade = IntegerField(max_value=10, min_value=0)

    required = {"required": "required", "class": "form-group col-md-6 form-control"}
    name_attrs = {"type": "text", "placeholder": "Your Name", "name": "name"} | required
    email_attrs = {"type": "email", "placeholder": "Email Address"} | required
    text_attrs = {"name": "text", "placeholder": "Text"} | required

    name.widget.attrs.update(name_attrs)
    email.widget.attrs.update(email_attrs)
    text.widget.attrs.update(text_attrs)
