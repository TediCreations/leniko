# Generated by Django 3.1.4 on 2021-03-06 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_delete_cart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
