# Generated by Django 4.1.7 on 2023-04-17 19:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LykaAccounts', '0003_alter_customer_uid'),
        ('LykaCart', '0003_cart_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='LykaAccounts.customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='date_added',
            field=models.DateField(default=datetime.date(2023, 4, 18)),
        ),
    ]
