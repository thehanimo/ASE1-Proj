from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from orders.models import Order
from userAuth.models import User
from agents.models import Agent
from customers.models import Customer
from executives.models import Executive
from shop.models import Product, Category


class AgentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2
        if commit:
            user.save()
        return user

class AgentSignUpFormExtended(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = Agent
        fields = ('email', 'fullname', 'phone', 'area', 'rating')

class AgentDetailsForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('fullname', 'phone', 'area', 'rating')

    def save(self, user=None):
        agent_details = super(AgentDetailsForm, self).save(commit=False)
        if user:
            agent_details.user = user
        agent_details.save()
        return agent_details

    def dummy_phone_save(self, user, phone):
        agent = Agent.objects.get(user=user)
        agent.phone = phone 
        agent.save()

class AgentDeleteForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Agent
        fields = ('check',)

    def save(self, user=None):
        agent = Agent.objects.get(user=user)
        agent.delete()
        user.delete()
        return