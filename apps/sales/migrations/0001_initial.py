# Generated by Django 4.1.7 on 2023-03-10 06:50

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, editable=False, max_length=30, unique=True)),
                ('status', models.CharField(choices=[('new', 'new'), ('printed', 'printed'), ('picked', 'picked'), ('delivered', 'delivered')], default='new', max_length=30)),
                ('packing_slip_file', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/pdf'), upload_to='packing_slips/')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_products', to='sales.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.seller'),
        ),
    ]