# Generated by Django 3.1 on 2024-07-21 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_wishlist', '0002_wishlistitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='wishlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_wishlist.wishlist'),
        ),
    ]
