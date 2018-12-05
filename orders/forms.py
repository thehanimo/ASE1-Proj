from django import forms
from .models import Order
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from orders.models import Order
from userAuth.models import User
from agents.models import Agent
from customers.models import Customer
from executives.models import Executive
from shop.models import Product, Category


class CheckoutForm(forms.ModelForm):
	preferred_time=forms.CharField()
	class Meta:
		model = Order
		fields = ('payment_type', )
		


class OrderCancelForm(forms.ModelForm):
	check = forms.BooleanField()
	class Meta:
		model = Order
		fields = ('check',)

	def save(self, order=None):
		order = Order.objects.get(id=order.id)
		order.order_status = 'W'
		order.save()
		return

class OrderCancelConfirmForm(forms.ModelForm):
	check = forms.BooleanField()
	class Meta:
		model = Order
		fields = ('check',)

	def save(self, order=None):
		order = Order.objects.get(id=order.id)
		order.order_status = 'X'
		order.save()
		return

class OrderAcceptForm(forms.ModelForm):
	check = forms.BooleanField()
	class Meta:
		model = Order
		fields = ('check',)

	def save(self, order=None):
		order = Order.objects.get(id=order.id)
		order.order_status = '2'
		order.save()
		return

class OrderOutForDeliveryForm(forms.ModelForm):
	check = forms.BooleanField()
	class Meta:
		model = Order
		fields = ('check',)

	def save(self, order=None):
		order = Order.objects.get(id=order.id)
		order.order_status = '3'
		order.save()
		return

class OrderDeliveredForm(forms.ModelForm):
	check = forms.BooleanField()
	class Meta:
		model = Order
		fields = ('check',)

	def save(self, order=None):
		order = Order.objects.get(id=order.id)
		order.order_status = '4'
		order.save()
		return
