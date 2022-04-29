from django.forms import ModelForm, RadioSelect, ModelChoiceField, TextInput, EmailInput, Textarea

from Shop.models import Review, RatingGrade


class ReviewForm(ModelForm):
    """Добавление отзыва к карточке продукта"""
    grade = ModelChoiceField(
        queryset=RatingGrade.objects.all(),
        widget=RadioSelect(),
        empty_label=None,
    )

    class Meta:
        """Рендеринг формы для captcha"""
        pattern = {"class": "form-group col-md-6 form-control"}
        name_attrs = {"type": "text", "placeholder": "Ваше имя", "name": "name"} | pattern
        email_attrs = {"type": "email", "placeholder": "Адрес электронной почты"} | pattern
        text_attrs = {"name": "text", "placeholder": "Текст"} | pattern

        model = Review
        fields = ('name', 'email', 'text', 'ipaddress', 'product', 'grade')

        widgets = {
            'name':  TextInput(attrs=name_attrs),
            'email':  EmailInput(attrs=email_attrs),
            'text': Textarea(attrs=text_attrs),
        }
