from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
from utils.django_models.field_choices import create_choices_tuple
from apps.sales.logic import (calculate_total_price, calculate_total_weight, calculate_total_seller_commission,
                              define_order_code, calculate_order_total_price, calculate_order_total_weight,
                              calculate_order_total_seller_commission, get_pipeline_details)
from apps.tasks_pipeline.tasks import pipeline_runner

status = ('new', 'printed', 'picked', 'delivered')


class Seller(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class OrderedProduct(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField()
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE, related_name='ordered_products')

    def total_price(self):
        return calculate_total_price(self.product.price, self.quantity)

    def total_price_fmt(self):
        return '${0:.2f}'.format(self.total_price())

    def total_weight(self):
        return calculate_total_weight(self.product.weight, self.quantity)

    def total_weight_fmt(self):
        return '{0:.2f}lb'.format(self.total_weight())

    def total_seller_commission(self):
        return calculate_total_seller_commission(self.total_price(), self.product.seller_commission_tax)

    def total_seller_commission_fmt(self):
        return '{0:.2f}%'.format(self.total_seller_commission(self))

    def __str__(self):
        return f'{self.product.name}: {self.quantity}'


class Order(models.Model):
    code = models.CharField(max_length=30, unique=True, blank=True, editable=False)
    status = models.CharField(max_length=30, choices=create_choices_tuple(status), default='new')
    customer = models.ForeignKey('customer.Customer', on_delete=models.PROTECT)
    seller = models.ForeignKey('sales.Seller', on_delete=models.PROTECT)

    packing_slip_file = models.FileField(null=True, blank=True, editable=False,
                                         storage=FileSystemStorage(location=settings.MEDIA_ROOT))

    created_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)

    def __str__(self):
        return self.code

    def order_ordered_products(self):
        return self.ordered_products.all()

    def order_total_price(self):
        return calculate_order_total_price(self)

    def order_total_price_fmt(self):
        return '${0:.2f}'.format(self.order_total_price())

    def order_total_weight(self):
        return calculate_order_total_weight(self)

    def order_total_weight_fmt(self):
        return '{0:.2f}lb'.format(self.order_total_weight())

    def order_total_seller_commission(self):
        return calculate_order_total_seller_commission(self)

    def order_total_seller_commission_fmt(self):
        return '{0:.2f}%'.format(self.order_total_seller_commission(self))

    def get_pipeline_details(self):
        return get_pipeline_details(self)

    def save(self, *args, **kwargs):
        # creating SKU code
        if not self.code:
            self.code = define_order_code(self.customer.customer_type)
        super().save(*args, **kwargs)


@receiver(post_save, sender=Order, dispatch_uid="trigger_to_run_pipeline")
def trigger_to_run_pipeline(sender, instance, created, **kwargs):
    if created:
        pipeline_runner.apply_async(kwargs={'model_class_ref': 'sales.Order',
                                            'model_instance_pk': instance.pk},
                                    countdown=0.5)
