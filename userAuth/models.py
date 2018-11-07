from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

def upload_path_handler(instance, filename):
    import os.path
    fn, ext = os.path.splitext(filename)
    return "{id}{ext}".format(id=instance.pk, ext=ext)

class User(AbstractUser):
	USER_TYPE_CHOICES = (
	  (1, 'customer'),
	  (2, 'agent'),
	  (3, 'executive'),
	  (5, 'admin'),
  )
	user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=5)

class Agent(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50)
	photo = models.ImageField(upload_to=upload_path_handler, blank=True)
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	street = models.CharField(max_length=100, default='')
	area = models.CharField(max_length=100, default='')

class Executive(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

	

