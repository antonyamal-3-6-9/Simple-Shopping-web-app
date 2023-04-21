# Generated by Django 4.1.7 on 2023-04-17 11:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LykaAccounts', '0002_customer_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
