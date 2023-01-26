from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name='owned_rooms')
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User, related_name='joined_rooms', blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'messages')
    room = models.ForeignKey(Room, on_delete = models.CASCADE, related_name = 'messages')
    body = models.TextField()
    updated = models.DateTimeField(auto_now =True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.body[:50]}..."  if len(self.body) > 50 else self.body                           