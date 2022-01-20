from django.contrib import admin
from django.utils.safestring import mark_safe

from mptt.admin import MPTTModelAdmin

from Blog.models import News, Comment
from Blog.forms import NewsAdminForm


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Новости и события на странице /blog/"""
    list_display = ('id', 'title', 'date', 'time', 'is_draft', 'get_poster', 'creator')
    readonly_fields = ('get_poster',)
    list_display_links = ('id', 'title')
    list_filter = ('creator',)
    search_fields = ('title', 'description')
    save_as = True
    save_as_continue = False
    list_per_page = 30
    save_on_top = True
    actions_on_bottom = True
    actions = ['publish', 'un_publish', 'is_draft']
    form = NewsAdminForm

    def is_draft(self, obj):
        """Иконки статуса публикации вместо галочек"""
        return obj.draft is False

    is_draft.boolean = True
    is_draft.short_description = 'Черновик'

    def publish(self, request, queryset):
        """user action - Уведомление о публикации"""
        count_obj = queryset.update(draft=False)
        if count_obj == 1:
            message = '1 запись была опубликована'
        else:
            message = f'{count_obj} записей были опубликованы'
        self.message_user(request, f"{message}")

    def un_publish(self, request, queryset):
        """user action -  Уведомления о снятии с публикации"""
        count_obj = queryset.update(draft=True)
        if count_obj == 1:
            message = "1 запись была обновлена"
        else:
            message = f"{count_obj} записей были обновлены"
        self.message_user(request, f"{message}")

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    un_publish.short_description = "Снять с публикации"
    un_publish.allowed_permissions = ('change',)

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="70" height="30"')

    get_poster.short_description = 'Постер'


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('creator', 'text', 'parent', 'news', 'created')
