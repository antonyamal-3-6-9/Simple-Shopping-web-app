# Generated by Django 4.1.7 on 2023-04-21 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LykaAccounts', '0009_alter_cardpaymentdetails_cardowner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upipaymentdetails',
            name='upiOwner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LykaAccounts.customer'),
        ),
    ]