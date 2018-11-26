from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from orders.models import Order
from .models import User
from agents.models import Agent
from customers.models import Customer
from executives.models import Executive
from shop.models import Product, Category


class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class NewPasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1', 'password2')

    def save(self, user=None):
        if user:
            user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

class AgentSignUpForm(forms.Form):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('fullname', 'email', 'phone', 'area')