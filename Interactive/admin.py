from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin, FlatPage
from django.utils.safestring import mark_safe

from Interactive.models import Delivery, Customer, Mail

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('email', 'date')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('address_header', 'user', 'email')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'get_avatar')
    save_on_top = True
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('get_avatar',)

    def get_avatar(self, obj):
        return mark_safe(f'<img src={obj.avatar.url} width="110" height="80"')

    get_avatar.short_description = 'Аватар'


class FlatPageAdmin(FlatPageAdmin):
    """Переопределение и изменение стандартной панели плоских страниц"""
    # from django.utils.translation import gettext_lazy as _
    fieldsets = (
        (None,
         {
             'fields': ('url', 'title', 'content', 'sites', 'registration_required', 'template_name')
         }),
    )
