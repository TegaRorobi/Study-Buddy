from rest_framework import serializers
from main.models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

# from django import forms
# from .models import *

# class RoomForm(forms.ModelForm):
    # class Meta:
    #     model = Room
    #     fields = '__all__'