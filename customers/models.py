from django.db import models
from userAuth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

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


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50, validators=[alphabets])
	photo = models.ImageField(upload_to=upload_path_handler, blank=True)
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	area = models.CharField(max_length=6, default='', choices=AREA_CHOICES)
	street = models.CharField(max_length=100, default='')