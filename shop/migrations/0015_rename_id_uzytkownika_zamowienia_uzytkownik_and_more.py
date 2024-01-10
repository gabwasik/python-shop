# Generated by Django 4.2 on 2023-06-15 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_rename_id_plyty_szczegolyzamowienia_plyta_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zamowienia',
            old_name='id_uzytkownika',
            new_name='uzytkownik',
        ),
        migrations.AlterField(
            model_name='szczegolyzamowienia',
            name='plyta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.plyty'),
        ),
        migrations.AlterField(
            model_name='szczegolyzamowienia',
            name='zamowienie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.zamowienia'),
        ),
    ]
