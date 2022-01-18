from django.forms import Textarea, ModelForm, CharField

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from Blog.models import Comment, News


class AddCommentForm(ModelForm):
    """Добавление комментария к новости"""

    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'text': Textarea(attrs={"id": "commentator"})}


class NewsAdminForm(ModelForm):
    """CKEditor"""
    description = CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'
