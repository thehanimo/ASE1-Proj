from django import forms
from .models import Order, Tracking
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from orders.models import Order
from userAuth.models import User
from agents.models import Agent
from customers.models import Customer
from executives.models import Executive
from shop.models import Product, Category
from .models import PartyOrders, BILLING_TYPES


class CheckoutForm(forms.Form):
	payment_type = forms.CharField()
	preferred_time=forms.CharField()
	class Meta:
		model = Order
		


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
		try:
			tracking = Tracking.objects.get(order=order)
			tracking.enabled=True
		except:
			tracking = Tracking.objects.create(order=order, enabled=True)
		tracking.save()
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
		order.paid = True
		tracking = Tracking.objects.get(order=order)
		tracking.delete()
		order.save()
		return

class PartyOrderCreateForm(forms.ModelForm):
    class Meta:
        model = PartyOrders
        fields = ('number_of_cans','comments')

    def save(self, user):
        order = PartyOrders.objects.create(
            user=user,
            number_of_cans=self.cleaned_data['number_of_cans'],
            comments=self.cleaned_data['comments'],
            )
        order.save()