from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import OrderItem, Order
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from userAuth.models import Agent

from .decorators import customer_required, customer_details_required

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

@login_required
@customer_required
@customer_details_required
def order_create(request):
    if request.method == 'POST':
        cart = Cart(request)
        try:
            agent = Agent.objects.get(area=request.user.customer.area)
            if agent.user.is_active == False:
                raise Agent.DoesNotExist
        except Agent.DoesNotExist:
            return render(request, 'orders/order/NoDelivery.html', {'area':request.user.customer.get_area_display()})
        order = Order.objects.create(customer=request.user, agent=agent.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
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