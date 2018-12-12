from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from cart.cart import Cart
from django.http import HttpResponseRedirect
from orders.models import Order
from . import Checksum

from .models import PaytmHistory
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from InvoiceGenerator.create import create_invoice
from aseproject.settings import MEDIA_ROOT


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.


def payment(request):
    cart = Cart(request)
    bill_amount = cart.get_total_price()
    cart.clear()
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = 'http://'+get_current_site(request).domain + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = Checksum.__id_generator__()
    if bill_amount:
        data_dict = {
                    'MID':MERCHANT_ID,
                    'ORDER_ID':order_id,
                    'TXN_AMOUNT': bill_amount,
                    'CUST_ID':'harish@pickrr.com',
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE': settings.PAYTM_WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':CALLBACK_URL,
                }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        print('a', param_dict)
        return render(request,"paytm/payment.html",{'paytmdict':param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")

@csrf_exempt
def response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        print('b', data_dict)
        verify = Checksum.verify_checksum(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            print(verify)
            PaytmHistory.objects.create(**data_dict)
            print(data_dict)
            return render(request, "paytm/response.html", {"paytm":data_dict})
        else:
            print("no")
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

def status(request):
    data_dict = {}
    for key in request.POST:
        data_dict[key] = request.POST[key]
    print(data_dict)
    context = {'resultDict': data_dict}
    if data_dict['STATUS'] == 'TXN_SUCCESS':
        oid = order_create(request)
        if oid == 'S':
            return render(request, 'paytm/success.html', {'cart':Cart(request)})
        return HttpResponseRedirect('/orders/placed/'+oid)
    return render(request, 'paytm/failed.html', context )



def order_create(request):
    try:
        order = Order.objects.filter(customer=request.user,order_status='P').first()
        oid = urlsafe_base64_encode(force_bytes(order.id)).decode()
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
        order.order_status = '1'
        order.save()
    except:
        oid = 'S'
    return oid