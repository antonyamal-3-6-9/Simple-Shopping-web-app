# Generated by Django 4.1.7 on 2023-04-17 09:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LykaCart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_added',
            field=models.DateField(default=datetime.date(2023, 4, 17)),
        ),
    ]