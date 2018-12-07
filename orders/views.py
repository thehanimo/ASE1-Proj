from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from .models import OrderItem, Order
from cart.cart import Cart
from shop.models import Product
from django.contrib.auth.decorators import login_required
from agents.models import Agent

from userAuth.decorators import customer_required, customer_details_required

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .forms import CheckoutForm

from InvoiceGenerator.create import create_invoice
from aseproject.settings import MEDIA_ROOT


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


@login_required
@customer_required
@customer_details_required
def order_create(request):
    cart = Cart(request)
    form = CheckoutForm()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if cart.get_total_price() == 0:
            return redirect('cart:cart_detail')
        if form.is_valid():
            try:
                agent = Agent.objects.get(area=request.user.customer.area)
                if agent.user.is_active == False:
                    raise Agent.DoesNotExist
            except Agent.DoesNotExist:
                return render(request, 'orders/order/NoDelivery.html', {'area':request.user.customer.area})
            preferred_time = form.cleaned_data['preferred_time']
            order = Order.objects.create(customer=request.user, agent=agent.user, payment_type=form.cleaned_data['payment_type'], preferred_time=preferred_time)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                item['product'].reduce_stock(item['quantity'])
                item['product'].save()
            cart.clear()
            order.save()
            oid = urlsafe_base64_encode(force_bytes(order.id)).decode()
            return HttpResponseRedirect('/orders/placed/'+oid)
    return render(request, 'orders/order/create.html', {'form':form,'cart': cart})

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
        create_invoice(request.user, order)
        current_site = get_current_site(request)
        mail_subject = 'Your Order.'
        message = render_to_string('email/order_suc.html')
        to_email = request.user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.attach_file(MEDIA_ROOT+'/orders/'+str(order.id)+".pdf")
        email.send()
        return render(request, 'orders/order/created.html', {'order': order})
    return render(request, '500.html')

