from django.db import models
from userAuth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator

alphabets = RegexValidator(r'^[ a-zA-Z]*$', 'Only alphabets are allowed.')
zipcode_validator = RegexValidator(r'^[0-9]{6}$', 'Only 6-digit zipcodes supported.')


class Agent(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50, validators=[alphabets])
	phone = PhoneNumberField(null=False, blank=False, unique=True)
	zipcode = models.CharField(max_length=6, default='', validators=[zipcode_validator])
	area = models.CharField(max_length=30, default='', validators=[alphabets])
	rating = models.FloatField(default=0,validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
	no_of_ratings = models.IntegerField(default=0)