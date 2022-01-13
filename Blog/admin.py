from django.contrib import admin
from Blog.models import Comment
from django import forms

from mptt.admin import MPTTModelAdmin
from Blog.models import News
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Новости и события на странице /blog/"""
    list_display = ('id', 'title', 'date', 'time', 'draft', 'poster', 'creator',)
    list_filter = ('creator', 'draft',)
    search_fields = ('title', 'description')
    save_as = True
    save_as_continue = False
    list_per_page = 30
    save_on_top = True
    actions_on_bottom = True
    list_editable = ('draft',)
    form = NewsAdminForm


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('creator', 'text', 'parent', 'news', 'created')
