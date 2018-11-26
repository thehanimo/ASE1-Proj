from django.db import models
from userAuth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

alphabets = RegexValidator(r'^[ a-zA-Z]*$', 'Only alphabets are allowed.')
zipcode_validator = RegexValidator(r'^[0-9]{6}$', 'Only 6-digit zipcodes supported.')

def upload_path_handler(instance, filename):
	import os.path
	fn, ext = os.path.splitext(filename)
	return "{id}{ext}".format(id=instance.pk, ext=ext)


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50, validators=[alphabets])
	photo = models.ImageField(upload_to=upload_path_handler, blank=True)
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	zipcode = models.CharField(max_length=6, default='', validators=[zipcode_validator])
	street = models.CharField(max_length=100, default='')
	area = models.CharField(max_length=30, default='', validators=[alphabets])