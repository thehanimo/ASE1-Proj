from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *

@receiver(post_save, sender=MyCustomUser)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
  if created:
    profile = MyProfile(user=instance)
    profile.save()