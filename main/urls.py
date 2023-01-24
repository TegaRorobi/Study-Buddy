from django.urls import path
from .views import *


app_name='main'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'), 
    path('contact/', contact, name='contact'),
    path('create-room/', createRoom2.as_view(), name = 'create-room'),
    path('update-room/<int:pk>/', updateRoom2.as_view(), name = 'update-room'),
    path('delete-room/<int:pk>/', deleteRoom.as_view(), name = 'delete-room'),
]

