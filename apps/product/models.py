from django.db import models
from apps.product.logic import define_sku_code


class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    pipeline = models.ForeignKey('tasks_pipeline.Pipeline', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    product_type = models.ForeignKey('product.ProductType', on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    weight = models.FloatField()
    price = models.FloatField()
    seller_commission_tax = models.FloatField()

    def __str__(self):
        return f'{self.name}: ${self.price}'

    @property
    def price_fmt(self):
        return f'${self.price}'

    @property
    def weight_fmt(self):
        return f'{self.weight}lb'

    def save(self, *args, **kwargs):
        # creating SKU code
        if not self.sku:
            self.sku = define_sku_code(self.product_type.name)
        super().save(*args, **kwargs)
