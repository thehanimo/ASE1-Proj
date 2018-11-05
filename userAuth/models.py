from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	USER_TYPE_CHOICES = (
      (1, 'customer'),
      (2, 'agent'),
      (3, 'executive'),
  )
	user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

class Agent(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Executive(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

	

