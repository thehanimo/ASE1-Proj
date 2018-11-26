from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

alphabets = RegexValidator(r'^[ a-zA-Z]*$', 'Only alphabets are allowed.')
zipcode_validator = RegexValidator(r'^[0-9]{6}$', 'Only 6-digit zipcodes supported.')

USER_TYPE_CHOICES = (
	  (1, 'customer'),
	  (2, 'agent'),
	  (3, 'executive'),
	  (5, 'admin'),
	  )

def upload_path_handler(instance, filename):
	import os.path
	fn, ext = os.path.splitext(filename)
	return "{id}{ext}".format(id=instance.pk, ext=ext)


class User(AbstractUser):
	user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=5)
	email = models.EmailField(('email address'), blank=False, unique=True)
	email_verified = models.BooleanField(default=False)

class AgentApplications(models.Model):
	fullname = models.CharField(max_length=50, validators=[alphabets])
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	zipcode = models.CharField(max_length=6, default='', validators=[zipcode_validator])
	area = models.CharField(max_length=30, default='', validators=[alphabets])
	email = models.EmailField(('email address'), blank=False, unique=True)