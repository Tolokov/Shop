from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from Blog.models import Comment, News


class AddCommentForm(forms.ModelForm):
    """Добавление комментария к новости"""

    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'text': forms.Textarea(attrs={"id": "commentator"})}


class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'
