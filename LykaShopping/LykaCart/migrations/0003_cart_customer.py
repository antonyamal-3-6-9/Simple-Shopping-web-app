# Generated by Django 4.1.7 on 2023-04-17 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LykaAccounts', '0001_initial'),
        ('LykaCart', '0002_alter_cart_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='LykaAccounts.customer'),
        ),
    ]
