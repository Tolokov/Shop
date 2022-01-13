from django.contrib import admin

import Interactive.models
from Interactive.models import Delivery, Customer


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('address_header', 'user', 'email')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'email')
    save_on_top = True
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('first_name', 'last_name', 'phone', 'email')
