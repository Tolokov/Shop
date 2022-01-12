from django.forms import Form,  CharField, Textarea, EmailField, IntegerField


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
