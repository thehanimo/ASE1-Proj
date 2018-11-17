from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import OrderItem, Order
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

from .decorators import customer_required, customer_details_required

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

@login_required
@customer_required
@customer_details_required
def order_create(request):
    if request.method == 'POST':
        cart = Cart(request)
        order = Order.objects.create(customer=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        order.save()
        oid = urlsafe_base64_encode(force_bytes(order.id)).decode()
        return HttpResponseRedirect('/orders/placed/'+oid)
    return render(request, '500.html')

@login_required
@customer_required
@customer_details_required
def order_complete(request, uidb64):
    try:
        oid = force_text(urlsafe_base64_decode(uidb64))
        order = Order.objects.get(pk=oid)
    except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
        order = None
    if order:
        return render(request, 'orders/order/created.html', {'order': order})
    return render(request, '500.html')