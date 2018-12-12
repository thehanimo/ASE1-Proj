from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from orders.models import Order
from userAuth.models import User
from agents.models import Agent
from customers.models import Customer
from executives.models import Executive
from shop.models import Product, Category


class CategoryDeleteForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Category
        fields = ('check',)

    def save(self, in_cat=None):
        cat = Category.objects.get(id=in_cat.id)
        cat.delete()
        return

class CategorySignUpForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','slug')

    def save(self):
        cat = Category.objects.create(slug=self.cleaned_data['slug'], name=self.cleaned_data['name'])
        cat.save()

class ProductSignUpForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','name','slug','description','price','available','stock','image','number_of_cans','only_online')

    def save(self):
        prod = Product.objects.create(
            category=self.cleaned_data['category'],
            slug=self.cleaned_data['slug'],
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            price=self.cleaned_data['price'],
            available=self.cleaned_data['available'],
            stock=self.cleaned_data['stock'],
            image=self.cleaned_data['image'],
            )
        a=prod.reduce_stock(0)
        prod.save()

class ProductDeleteForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Product
        fields = ('check',)

    def save(self, in_prd=None):
        prd = Product.objects.get(id=in_prd.id)
        prd.delete()
        return

class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','name','slug','description','price','available','stock','image','number_of_cans','only_online')

    def save(self, user=None):
        product_details = super(ProductDetailsForm, self).save(commit=False)
        product_details.save()
        return product_details
