from django.urls import path
from .views import *


app_name='main'
urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('home/', HomeView.as_view(), name='home'), 
    path('contact/', contact, name='contact'),
    path('create-room/', createRoom.as_view(), name = 'create-room'),
    path('update-room/<int:pk>/', updateRoom.as_view(), name = 'update-room'),
    path('delete-room/<int:pk>/', deleteRoom.as_view(), name = 'delete-room'),
]

