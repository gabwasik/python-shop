from django.urls import path, re_path
from . import views

urlpatterns = [
    # główne linki
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('orders/', views.orders, name='orders'),
    path('statistics/', views.statistics, name='statistics'),
    path('register/', views.register, name='register'),

    # sklep
    path('product/<int:num>/', views.product, name='product'),
    path('product/add/', views.product_add, name='product_add'),
    path('cart', views.cart_detail, name='cart-detail'),
    path('cart/item-clear/<int:product_id>/', views.item_clear, name='item-clear'),
    path('cart/item-increment/<int:product_id>/<int:quantity>/', views.item_increment, name='item-increment'),
    path('cart/item-decrement/<int:product_id>/<int:quantity>/', views.item_decrement, name='item-decrement'),
    path('cart/clear/', views.cart_clear, name='cart-clear'),
    path('cart/order/', views.cart_order, name='cart-order'),
    re_path(r'^cart/add/(?P<product_id>\d+)/(?P<quantity>[1-9]\d*)/$', views.cart_add, name='cart-add'),
]
