# Generated by Django 4.2 on 2023-06-15 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_rename_id_uzytkownika_zamowienia_uzytkownik_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='szczegolyzamowienia',
            options={'ordering': ['zamowienie_id'], 'verbose_name': 'szczegóły zamówienia', 'verbose_name_plural': 'szczegóły zamówienia'},
        ),
        migrations.AddField(
            model_name='plyty',
            name='sprzedano',
            field=models.IntegerField(default=0, verbose_name='Ilość sprzedanych sztuk'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plyty',
            name='ilosc',
            field=models.IntegerField(verbose_name='Ilość sztuk na stanie'),
        ),
    ]