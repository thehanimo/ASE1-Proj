from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from phonenumber_field.formfields import PhoneNumberField

from userAuth.models import Agent, Customer, Executive, User

class AgentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2
        if commit:
            user.save()
        return user

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

class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('fullname', 'photo', 'phone', 'street', 'area')

    def save(self, user=None):
        customer_details = super(CustomerDetailsForm, self).save(commit=False)
        if user:
            customer_details.user = user
        customer_details.save()
        return customer_details

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
