# Generated by Django 4.1.7 on 2023-04-18 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LykaAccounts', '0005_remove_customer_order_customer_defaultaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='defaultaddress',
        ),
    ]
