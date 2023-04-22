from django.conf import settings
from django.views.generic.detail import DetailView
from django.urls import path, reverse
from django.utils.html import format_html
from admin_site import admin
from apps.sales.models import Seller, Order, OrderedProduct
from apps.tasks_pipeline.tasks import pipeline_runner


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class OrderedProductInLine(admin.TabularInline):
    model = OrderedProduct
    extra = 0
    min_num = 1
    autocomplete_fields = ('product',)


class OrderDetailView(DetailView):
    template_name = "packing_slip/detail.html"
    model = Order

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs),
                **admin.site.each_context(self.request),
                "opts": self.model._meta}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # listing view
    list_display = ('code', 'customer', 'status', 'seller', 'total_weight', 'total_price',
                    'total_seller_commission', 'order_created_at', 'packing_slip_details')
    search_fields = ('customer__name',)
    ordering = ('-id',)
    list_filter = ('status', 'seller')

    # listing actions
    actions = ('set_order_as_printed', 'set_order_as_picked', 'set_order_as_delivered', 'run_order_pipeline_again')

    # create/edit view
    autocomplete_fields = ('customer', 'seller')
    inlines = (OrderedProductInLine,)

    def total_price(self, obj):
        return '${0:.2f}'.format(obj.order_total_price())

    def total_weight(self, obj):
        return '{0:.2f}lb'.format(obj.order_total_weight())

    def total_seller_commission(self, obj):
        return '${0:.2f}'.format(obj.order_total_seller_commission())

    def order_created_at(self, obj):
        return obj.created_at.strftime(settings.DEFAULT_TIME_FORMAT)

    @admin.action(description='Set (new) orders as (printed)')
    def set_order_as_printed(self, request, queryset):
        queryset.filter(status='new').update(status='printed')

    @admin.action(description='Set (printed) orders as (picked)')
    def set_order_as_picked(self, request, queryset):
        queryset.filter(status='printed').update(status='picked')

    @admin.action(description='Set (picked) orders as (delivered)')
    def set_order_as_delivered(self, request, queryset):
        queryset.filter(status='picked').update(status='delivered')

    @admin.action(description='Run tasks from order pipeline again')
    def run_order_pipeline_again(self, request, queryset):
        for order in queryset.all():
            pipeline_runner.delay(model_class_ref='sales.Order', model_instance_pk=order.pk)

    def get_urls(self):
        return [path("<pk>/detail",
                     self.admin_site.admin_view(OrderDetailView.as_view()),
                     name=f"sales_order_detail"),
                *super().get_urls()]

    def packing_slip_details(self, obj):
        url = reverse("admin:sales_order_detail", args=[obj.pk])
        return format_html(f'<a href="{url}">📝</a>')
