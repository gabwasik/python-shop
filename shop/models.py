import os
from django.contrib.auth.models import User
from django.db import models


class Plyty(models.Model):
    RODZAJE = (('CD', 'Płyta CD'), ('winyl', 'Winyl'), ('kaseta', 'Kaseta magnetofonowa'))

    rodzaj = models.TextField('Rodzaj', choices=RODZAJE, default='CD')
    okladka = models.FileField('Okładka')
    tytul = models.CharField('Tytuł', max_length=64)
    wykonawca = models.CharField('Wykonawca', max_length=64)
    ilosc_utworow = models.IntegerField('Ilość utworów')
    rok_wydania = models.IntegerField('Rok wydania')
    gatunek = models.CharField('Gatunek', max_length=64)
    opis = models.TextField('Opis')
    cena = models.DecimalField('Cena', max_digits=5, decimal_places=2)
    ilosc = models.IntegerField('Ilość sztuk na stanie')
    sprzedano = models.IntegerField('Ilość sprzedanych sztuk')

    class Meta:
        ordering = ['id']
        verbose_name = 'płyta'
        verbose_name_plural = 'płyty'

    def save(self, *args, **kwargs):
        super(Plyty, self).save(*args, **kwargs)
        os.rename(self.okladka.name, 'static/shop/img/product_{0}.jpg'.format(self.id))
        self.okladka = 'static/shop/img/product_{0}.jpg'.format(self.id)
        super(Plyty, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}. {1} – {2} ({3})'.format(self.id, self.wykonawca, self.tytul, self.rok_wydania)


class Zamowienia(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    data_zlozenia = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'zamówienie'
        verbose_name_plural = 'zamówienia'


class SzczegolyZamowienia(models.Model):
    zamowienie = models.ForeignKey(Zamowienia, on_delete=models.CASCADE)
    plyta = models.ForeignKey(Plyty, on_delete=models.CASCADE)
    cena = models.DecimalField('Cena', max_digits=5, decimal_places=2)
    ilosc = models.IntegerField('Ilość')

    class Meta:
        ordering = ['zamowienie_id']
        verbose_name = 'szczegóły zamówienia'
        verbose_name_plural = 'szczegóły zamówienia'

    def __str__(self):
        return 'Zamówienie #{}: {}x {} ({})'.format(self.zamowienie_id, self.ilosc,
                                                    self.plyta.tytul, self.plyta.rok_wydania)


class Wiadomosci(models.Model):
    imie = models.CharField('Imię', max_length=64)
    email = models.CharField('Adres e-mail', max_length=64)
    temat = models.CharField('Temat', max_length=64)
    tresc = models.TextField('Treść')

    class Meta:
        verbose_name = 'wiadomość'
        verbose_name_plural = 'wiadomości'

    def __str__(self):
        return '{0} ({1})'.format(self.temat, self.email)
