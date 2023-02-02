from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name='main'
urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('home/', HomeView.as_view(), name='home'), 
    # path('contact/', contact, name='contact'),
    path('room/<str:room_name>/', RoomView.as_view(), name='view-room'),
    path('create-room/', createRoom.as_view(), name = 'create-room'),
    path('update-room/<int:pk>/', updateRoom.as_view(), name = 'update-room'),
    path('delete-room/<int:pk>/', deleteRoom.as_view(), name = 'delete-room'),
    path('delete-message/<int:pk>/', deleteMessage.as_view(), name = 'delete-message'),
    path('profile/<str:username>/', UserProfile.as_view(), name = 'user-profile'), 
    path('update-profile/', updateUser.as_view(), name='update-profile'),
    path('topics/', TopicsView.as_view(), name='topics'),
    path('activity/', ActivityView.as_view(), name='activity'),
    # path('search/', search_results, name='ajax-search'),
]

