from django import forms
from django.views.decorators.debug import sensitive_variables
from captcha.fields import ReCaptchaField


@sensitive_variables('username', 'password')
class LoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=32)
    password = forms.CharField(label='Hasło', max_length=32)


class ContactForm(forms.Form):
    name = forms.CharField(label='Imię')
    email = forms.CharField(label='Adres e-mail')
    subject = forms.CharField(label='Temat')
    message = forms.CharField(label='Treść')
    captcha = ReCaptchaField()


class ProductForm(forms.Form):
    okladka = forms.FileField(label='Okładka')
    tytul = forms.CharField(label='Tytuł')
    rodzaj = forms.ChoiceField(label='Rodzaj', choices=(('CD', 'Płyta CD'), ('winyl', 'Winyl'), ('kaseta', 'Kaseta magnetofonowa')))
    cena = forms.FloatField(label='Cena')
    ilosc = forms.IntegerField(label='Ilość sztuk')
    wykonawca = forms.CharField(label='Wykonawca')
    rok_wydania = forms.IntegerField(label='Rok wydania')
    gatunek = forms.CharField(label='Gatunek')
    ilosc_utworow = forms.IntegerField(label='Ilość utworów')
    opis = forms.CharField(label='Opis')


class ProductEditForm(forms.Form):
    ilosc = forms.IntegerField(step_size=1)
