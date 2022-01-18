from django.forms import Textarea, IntegerField, TextInput, ModelForm
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from Shop.models import Review


class ReviewForm(ModelForm):
    """Добавление отзыва к карточке продукта"""
    captcha = ReCaptchaField()
    g = IntegerField(max_value=10, min_value=0)

    class Meta:
        """Рендеринг формы для captcha"""
        required = {"required": "required", "class": "form-group col-md-6 form-control"}
        name_attrs = {"type": "text", "placeholder": "Your Name", "name": "name"} | required
        email_attrs = {"type": "email", "placeholder": "Email Address"} | required
        text_attrs = {"name": "text", "placeholder": "Text"} | required

        model = Review
        fields = ('name', 'email', 'text', 'g', 'captcha')
        widgets = {
            'name':  TextInput(attrs=name_attrs),
            'email':  TextInput(attrs=email_attrs),
            'text': Textarea(attrs=text_attrs)
        }
