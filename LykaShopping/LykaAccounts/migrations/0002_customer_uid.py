# Generated by Django 4.1.7 on 2023-04-17 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LykaAccounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='uid',
            field=models.UUIDField(default=98),
            preserve_default=False,
        ),
    ]
