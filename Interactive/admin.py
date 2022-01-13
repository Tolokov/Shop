from django.contrib import admin
from django.utils.safestring import mark_safe

from Interactive.models import Delivery, Customer


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
