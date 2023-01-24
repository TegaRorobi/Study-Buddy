from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    model = Room
    list_display = ['name', 'description', 'created', 'updated']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    model = Topic
    list_display = ['name', 'created']