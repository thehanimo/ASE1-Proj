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
	class Meta(UserCreationForm.Meta):
		model = User

	def save(self, commit=True):
		user = super().save(commit=False)
		user.user_type = 1
		if commit:
			user.save()
		return user

class ExecutiveSignUpForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User

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