from django.contrib import admin
from Interactive.models import Customer
from Interactive.models import Delivery

admin.site.register(Customer)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('address_header', 'user', 'email')