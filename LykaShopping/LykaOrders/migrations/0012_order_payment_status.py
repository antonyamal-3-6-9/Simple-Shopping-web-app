# Generated by Django 4.1.7 on 2023-04-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LykaOrders', '0011_order_payment_method_order_tracking_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]