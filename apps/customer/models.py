from django.db import models
from django.utils import timezone
from utils.address.locations import cities, states, countries
from utils.django_models.field_choices import create_choices_tuple

client_types = ['individual', 'legal entity']


class Location(models.Model):
    city = models.CharField(max_length=150, null=True, blank=True)
    state = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150)

    def __str__(self):
        return ', '.join([self.city, self.state, self.country])


class Customer(models.Model):
    customer_type = models.CharField(max_length=30, choices=create_choices_tuple(client_types))
    name = models.CharField(max_length=255, unique=True)
    tax_id = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    location = models.ForeignKey('customer.Location', on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, blank=True)

    def __str__(self):
        return self.name
