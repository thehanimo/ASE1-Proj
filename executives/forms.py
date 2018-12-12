from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from orders.models import Order
from userAuth.models import User
from agents.models import Agent
from customers.models import Customer
from executives.models import Executive,AgentNotification
from shop.models import Product, Category
from orders.models import Subscriptions


class ExecutiveSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 3
        if commit:
            user.save()
        return user

class ExecutiveDetailsForm(forms.ModelForm):
    class Meta:
        model = Executive
        fields = ('photo',)

    def save(self, user=None):
        executive_details = super(ExecutiveDetailsForm, self).save(commit=False)
        if user:
            executive_details.user = user
        executive_details.save()
        return executive_details

class SubscriptionSignUpForm(forms.ModelForm):
    class Meta:
        model = Subscriptions
        fields = ('name','description', 'price', 'number_of_cans')

    def save(self):
        sub = Subscriptions.objects.create(
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            price=self.cleaned_data['price'],
            number_of_cans=self.cleaned_data['number_of_cans']
            )
        sub.save()

class AgentNotifyForm(forms.ModelForm):
    class Meta:
        model = AgentNotification
        fields = ('message',)
    def save(self, user=None):
        agent_notif = super(AgentNotifyForm, self).save(commit=False)
        agent_notif.save()
        return agent_notif