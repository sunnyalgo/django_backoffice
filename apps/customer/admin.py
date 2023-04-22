from django.conf import settings
from admin_site import admin
from apps.customer.models import Customer, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country')
    search_fields = ('city', 'state', 'country')
    ordering = ('city', 'state', 'country')
    list_filter = ('state', 'country')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_type', 'name', 'tax_id', 'location', 'customer_created_at')
    search_fields = ('name',)
    list_filter = ('customer_type', 'name',)
    ordering = ('customer_type', 'name',)
    autocomplete_fields = ('location', )

    def customer_created_at(self, obj):
        return obj.created_at.strftime(settings.DEFAULT_TIME_FORMAT)
