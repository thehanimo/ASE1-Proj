from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from orders.models import Order
from userAuth.models import User
from agents.models import Agent
from customers.models import Customer
from executives.models import Executive
from shop.models import Product, Category
from orders.models import Subscription, Subscriptions


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 1
        if commit:
            user.save()
        return user

class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('fullname', 'photo', 'phone', 'street', 'zipcode', 'area')

    def save(self, user=None):
        customer_details = super(CustomerDetailsForm, self).save(commit=False)
        if user:
            customer_details.user = user
        customer_details.save()
        return customer_details

class SubscriptionForm(forms.Form):
    subscription = forms.ChoiceField(choices=Subscriptions.objects.none(),widget=forms.RadioSelect)
    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['subscription'].choices = Subscriptions.get_all_subs()
    def save(self, user):
        sub = Subscriptions.objects.get(id=self.cleaned_data['subscription'])
        Subscription.objects.create(
            customer=user,
            subscription=sub.name,
            number_of_cans=sub.number_of_cans,
            )
        return self.cleaned_data['subscription']


