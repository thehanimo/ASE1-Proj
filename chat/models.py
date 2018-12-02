from django.db import models
from userAuth.models import User

class Room(models.Model):
    label = models.SlugField(unique=True)
    customer = models.ForeignKey(User, related_name='customer_room', on_delete=models.CASCADE, blank=True, null=True)
    executive = models.ForeignKey(User, related_name='executive_room', on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
