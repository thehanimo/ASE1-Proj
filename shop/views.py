from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

from userAuth.decorators import customer_required

@login_required
@customer_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, available=True)
    cart = Cart(request)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'cart':cart,
    }
    return render(request, 'shop/product/list.html', context)

@login_required
@customer_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    if product.stock < 5:
        qty_range = product.stock + 1
    else:
        qty_range = 6
    product_stock_list = [i for i in range(1,qty_range)]
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'cart':cart,
        'product_stock_list':product_stock_list
    }
    return render(request, 'shop/product/detail.html', context)

