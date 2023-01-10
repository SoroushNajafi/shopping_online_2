from django.shortcuts import render

from cart.cart import Cart
from cart.forms import AddToCartForm


def order_create_view(request):

    return render(request, 'orders/order_create.html',)
