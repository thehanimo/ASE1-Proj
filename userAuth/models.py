from django.db import models
from django.contrib.auth.models import AbstractUser

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
