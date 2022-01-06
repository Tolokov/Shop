from django import forms
from .models import Comment


class AddCommentForm(forms.ModelForm):
    """Добавление комментария к новости"""

    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={
                "required": "header",
                "id": "commentator",
            })}
