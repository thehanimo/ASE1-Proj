from django.db import models
from userAuth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

alphabets = RegexValidator(r'^[ a-zA-Z]*$', 'Only alphabets are allowed.')

def upload_path_handler(instance, filename):
	import os.path
	fn, ext = os.path.splitext(filename)
	return "{id}{ext}".format(id=instance.pk, ext=ext)


class Executive(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=50, validators=[alphabets])
	photo = models.ImageField(upload_to=upload_path_handler, blank=True)
	complaints_queue = models.IntegerField(default=0)

class AgentNotification(models.Model):
	agent = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	notified = models.BooleanField(default=False)