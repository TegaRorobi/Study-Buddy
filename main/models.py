from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

# Create your models here.

class User(AbstractUser):
    # username = models.CharField(max_length = 50)
    name = models.CharField(max_length = 100)
    # email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    # whenever you specify a default, django looks in the MEDIA_URL directory (which usually is the last bit of the url in the MEDIA_ROOT setting) 
    # the media url is the starting url for the links to the images displayed on the site and it can be named anything 
    # the media url gets its files from the media_root directory, but the name itself is what gets displayed in the urlbar in the website
    # in the settings which is currently 'media/' in the base directory.
    # django starts there and in the case below, we tell django to go further into 'user_images/' to get the image.
    image = models.ImageField(_('avatar'), upload_to = 'user_images', blank=True, null=True, default = 'user_images/default.png')

class Topic(models.Model):
    name = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name='owned_rooms')
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True, related_name = 'discussed_in')
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