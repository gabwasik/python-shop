from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.debug import sensitive_post_parameters

from .decorators import *
from .forms import *
from .models import *


def index(request):
    top3 = Plyty.objects.all().order_by('-sprzedano')[:3]
    return TemplateResponse(request, 'index.html', {'user': request.user, 'top3': top3})


def about(request):
    return TemplateResponse(request, 'about.html', {'user': request.user})


def shop(request):
    spis = Plyty.objects.all()
    return TemplateResponse(request, 'shop.html', {'user': request.user, 'spis': spis})


def contact(request):
    if request.method == 'POST':
        post = request.POST
        form = ContactForm(post)
        if form.is_valid():
            Wiadomosci(imie=post['name'], email=post['email'], temat=post['subject'], tresc=post['message']).save()
            return HttpResponseRedirect('/contact')
    else:
        form = ContactForm()

    return TemplateResponse(request, 'contact.html', {'user': request.user, 'form': form})


def product(request, num):
    plyta = Plyty.objects.get(id=num)
    if not plyta:
        raise Http404
    else:
        if request.method == 'POST':
            post = request.POST
            form = ProductEditForm(post)
            ilosc = post['ilosc']
            if form.is_valid() and ilosc and ilosc != plyta.id:
                Plyty.objects.filter(id=num).update(ilosc=ilosc)
                return HttpResponseRedirect('/product/{}'.format(plyta.id))
        else:
            form = ProductEditForm()

    return TemplateResponse(request, 'product.html', {'user': request.user, 'form': form,
                                                      'produkt': Plyty.objects.get(id=num), 'id': num})


@unauthenticated_user
@sensitive_post_parameters('username', 'password')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if 'login' in request.POST:
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/login')
    else:
        form = LoginForm()

    return TemplateResponse(request, 'login.html', {'user': request.user, 'form': form})


@unauthenticated_user
@sensitive_post_parameters('username', 'password', 'email')
def register(request):
    if request.method == 'POST':
        p = request.POST
        u = User.objects.create_user(username=p['username'], password=p['password'], email=p['email'])
        if not u:
            return HttpResponseRedirect('/register')

        u.first_name = p['name']
        u.last_name = p['surname']
        u.save()

        auth = authenticate(request, username=p['username'], password=p['password'])
        login(request, auth)
        return HttpResponseRedirect('/')

    return TemplateResponse(request, 'register.html', {'user': request.user})


########################################################################################################################
# Wymagające zalogowania się ###########################################################################################
########################################################################################################################


@login_required(login_url="/login")
def cart_add(request, product_id, quantity):
    cart = Cart(request)
    produkt = Plyty.objects.get(id=product_id)
    cart.add(product=produkt, quantity=quantity)
    return HttpResponseRedirect('/cart')


@login_required(login_url="/login")
def item_clear(request, product_id):
    cart = Cart(request)
    produkt = Plyty.objects.get(id=product_id)
    cart.remove(produkt)
    return HttpResponseRedirect('/cart')


@login_required(login_url="/login")
def item_increment(request, product_id, quantity):
    cart = Cart(request)
    produkt = Plyty.objects.get(id=product_id)
    cart.add(product=produkt, quantity=quantity)
    return HttpResponseRedirect('/cart')


@login_required(login_url="/login")
def item_decrement(request, product_id, quantity):
    cart = Cart(request)
    produkt = Plyty.objects.get(id=product_id)
    cart.decrement(product=produkt, quantity=quantity)
    return HttpResponseRedirect('/cart')


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return HttpResponseRedirect('/cart')


@login_required(login_url="/login")
def cart_detail(request):
    return TemplateResponse(request, 'cart.html', {'user': request.user})


@login_required(login_url="/login")
def cart_order(request):
    cart = Cart(request).cart
    order = Zamowienia(uzytkownik_id=request.user.id)
    order.save()

    for k, v in cart.items():
        product_id = v.get('product_id')
        quantity_new = v.get('quantity')
        SzczegolyZamowienia(zamowienie_id=order.id, plyta_id=product_id,
                            ilosc=quantity_new, cena=v.get('price')).save()

        album = Plyty.objects.get(id=product_id)
        quantity_old = album.ilosc
        sold_old = album.sprzedano
        Plyty.objects.filter(id=product_id).update(ilosc=int(quantity_old)-int(quantity_new),
                                                   sprzedano=int(sold_old)+int(quantity_new))

    return HttpResponseRedirect('/cart/clear')


@login_required(login_url="/login")
def orders(request):
    order = Zamowienia.objects.filter(uzytkownik_id=request.user.id).values_list('id', 'data_zlozenia')
    order_list = {}
    dates_list = {}

    for i in order:
        order_details = SzczegolyZamowienia.objects.filter(zamowienie_id=i[0])
        order_list[i[0]] = order_details
        dates_list[i[0]] = i[1].strftime('%Y-%m-%d, %H:%M:%S')

    return TemplateResponse(request, 'orders.html', {'user': request.user, 'orders': order_list, 'dates': dates_list})


########################################################################################################################
# Wymagające statusu administratora ####################################################################################
########################################################################################################################


@staff_member_required(login_url='/login')
def product_add(request):
    if request.method == 'POST':
        post = request.POST
        files = request.FILES
        form = ProductForm(post, files)
        if form.is_valid():
            Plyty(okladka=files['okladka'], tytul=post['tytul'], rodzaj=post['rodzaj'], cena=post['cena'],
                  ilosc=post['ilosc'], wykonawca=post['wykonawca'], rok_wydania=post['rok_wydania'],
                  gatunek=post['gatunek'], ilosc_utworow=post['ilosc_utworow'], opis=post['opis']).save()
            return HttpResponseRedirect('/shop')
    else:
        form = ProductForm()

    return TemplateResponse(request, 'product_add.html', {'user': request.user, 'form': form})


@staff_member_required(login_url='/login')
def statistics(request):
    if request.method == 'POST':
        post = request.POST
        month = post['miesiac']
        year = post['rok']

        orders_db = SzczegolyZamowienia.objects.select_related('zamowienie')
        sold = 0
        revenue = 0

        for i in orders_db:
            if i.zamowienie.data_zlozenia.month == int(month) and i.zamowienie.data_zlozenia.year == int(year):
                sold += i.ilosc
                revenue += i.cena * i.ilosc

        return TemplateResponse(request, 'statistics.html', {'user': request.user,
                                                             'statistics': (year, month, sold, revenue)})

    return TemplateResponse(request, 'statistics.html', {'user': request.user})
