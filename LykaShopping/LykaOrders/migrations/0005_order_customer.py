# Generated by Django 4.1.7 on 2023-04-18 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LykaAccounts', '0006_remove_customer_defaultaddress'),
        ('LykaOrders', '0004_order_deliveryaddress_order_deliverydate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LykaAccounts.customer'),
        ),
    ]