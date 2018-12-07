import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
from orders.models import OrderItem
from aseproject.settings import MEDIA_ROOT

def create_invoice(user, order):
    os.environ["INVOICE_LANG"] = "en"

    client_address = user.customer.street + ',<br/>' + user.customer.area
    client_zip_code = user.customer.zipcode
    client_phone = str(user.customer.phone)
    client_email = user.email

    provider_address = 'No.185, Bellman Ford St.' + ',<br/>' + 'T. Nagar'
    provider_zip_code = '600056'
    provider_phone = '044-42353988'
    provider_email = 'thewatercomp@gmail.com'
    payment_method = order.get_payment_type_display()

    client = Client(summary=user.customer.fullname, address=client_address, zip_code=client_zip_code, phone=client_phone,
                    email=client_email,)
    provider = Provider(summary='The Water Company', address=provider_address, zip_code=provider_zip_code, phone=provider_phone,
                        email=provider_email, payment_method=payment_method,
                        )
    creator = Creator('TWC')

    invoice = Invoice(client, provider, creator, str(order.id))
    invoice.currency_locale = 'en.UTF-8'
    items = OrderItem.objects.filter(order=order)
    for item in items:
        invoice.add_item(Item(item.quantity, item.price, description=item.product.name))

    pdf = SimpleInvoice(invoice)
    pdf.gen(MEDIA_ROOT+'/orders/'+str(order.id)+".pdf", generate_qr_code=False)