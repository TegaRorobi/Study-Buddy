from  django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class MyUserCreationForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['image', 'name', 'username', 'email', 'bio', 'password1', 'password2']


class MyUserUpdateForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['image', 'name', 'username', 'email', 'bio']