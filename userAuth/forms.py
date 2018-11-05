from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

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