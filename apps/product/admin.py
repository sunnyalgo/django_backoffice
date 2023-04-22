from admin_site import admin
from apps.product.models import Product, ProductType


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'pipeline')
    search_fields = ('name',)
    autocomplete_fields = ('pipeline',)
    ordering = ('id',)
    list_filter = ('pipeline',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product_type', 'name', 'product_weight', 'product_price', 'product_seller_commission_tax')
    autocomplete_fields = ('product_type',)
    search_fields = ('sku', 'name',)
    ordering = ('product_type', 'name',)
    list_filter = ('product_type',)

    def product_price(self, obj):
        return f'${obj.price}'

    def product_weight(self, obj):
        return f'{obj.weight}lb'

    def product_seller_commission_tax(self, obj):
        return f'{obj.weight}%'