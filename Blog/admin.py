from django.contrib import admin
from Blog.models import News, Comment

from mptt.admin import MPTTModelAdmin


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Новости и события на странице /blog/"""
    list_display = ('id', 'title', 'date', 'time', 'draft', 'poster', 'creator',)
    list_filter = ('creator', 'draft',)
    search_fields = ('title', 'description')
    save_as = True
    save_as_continue = False
    list_per_page = 30
    actions_on_bottom = True
    save_on_top = True
    list_editable = ('draft',)


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('creator', 'text', 'parent', 'news', 'created')
