# Generated by Django 3.1 on 2024-07-17 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin_account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=50),
        ),
    ]
