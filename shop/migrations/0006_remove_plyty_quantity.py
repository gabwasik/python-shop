# Generated by Django 4.2 on 2023-05-29 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_plyty_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plyty',
            name='quantity',
        ),
    ]
