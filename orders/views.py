from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem


@login_required
def order_create_view(request):
    cart = Cart(request)

    order_form = OrderForm()

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if len(cart) == 0:
            messages.warning(request, _('You can not proceed to checkout since your cart is empty'))
            return redirect('home')

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order_obj,
                    product=item['product_obj'],
                    quantity=item['quantity'],
                    price=item['product_obj'].price,
                )
            cart.clear()
            messages.success(request, _('Your Order has been submitted'))

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

    return render(request, 'orders/order_create.html', {'order_form': order_form})
