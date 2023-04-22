from django.db import models
from utils.django_models.field_choices import create_choices_tuple
from apps.financial.logic import calculate_royalties_gross_price

payment_status = ('new', 'approved', 'reproved', 'payed')


class SellerCommissionPayment(models.Model):
    order = models.OneToOneField('sales.Order', on_delete=models.PROTECT)
    status = models.CharField(max_length=30, default='new', choices=create_choices_tuple(payment_status))

    def __str__(self):
        return f'Commission for seller: {self.order.seller.name}'


class RoyaltiesPayment(models.Model):
    order = models.OneToOneField('sales.Order', on_delete=models.PROTECT)
    status = models.CharField(max_length=30, default='new', choices=create_choices_tuple(payment_status))

    def __str__(self):
        return f'Royalties for order: {self.order}'

    def royalties_gross_price(self):
        return calculate_royalties_gross_price(self.order)
