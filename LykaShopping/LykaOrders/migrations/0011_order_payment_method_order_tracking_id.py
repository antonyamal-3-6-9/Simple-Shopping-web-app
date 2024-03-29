# Generated by Django 4.1.7 on 2023-04-19 14:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LykaOrders', '0010_alter_address_phone_number_alter_address_zip_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tracking_id',
            field=models.CharField(default=uuid.uuid4, max_length=255),
        ),
    ]
