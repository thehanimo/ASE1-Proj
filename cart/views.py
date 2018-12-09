from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required

from userAuth.decorators import customer_required

@login_required
@customer_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)  # create a new cart object passing it the request object 
    product = get_object_or_404(Product, id=product_id) 
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('shop:product_detail',product.id,product.slug)

@login_required
@customer_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:product_list')

