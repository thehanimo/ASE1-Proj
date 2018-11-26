from .models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Product)
def check_availability(instance, **kwargs):
    if instance.stock <= 0:
    	instance.available = False
    else:
    	instance.available = True


