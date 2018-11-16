from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator, validate_email

alphabets = RegexValidator(r'^[ a-zA-Z]*$', 'Only alphabets are allowed.')

AREA_CHOICES = [
		('600018','Abhiramapuram'),
		('600020','Adyar'),
		('600040','Anna Nagar'),
	]

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
	email = models.EmailField(('email address'), blank=False, unique=True)
	email_verified = models.BooleanField(default=False)

class Agent(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50, validators=[alphabets])
	photo = models.ImageField(upload_to=upload_path_handler, blank=True)
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	area = models.CharField(max_length=6, default='', choices=AREA_CHOICES)
	rating = models.FloatField(default=0)

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50, validators=[alphabets])
	photo = models.ImageField(upload_to=upload_path_handler, blank=True)
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	area = models.CharField(max_length=6, default='', choices=AREA_CHOICES)
	street = models.CharField(max_length=100, default='')


class Executive(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50, validators=[alphabets])
	photo = models.ImageField(upload_to=upload_path_handler, blank=True)
	complaints_queue = models.IntegerField(default=0)
	

