from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import *
from .forms import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('main:home'))
        return render(request, 'main/login_register.html', {'action':'login'})
    def post(self, request):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully')
        else:
            messages.error(request, 'username or pasword does not exist')
        # print(request.META['HTTP_REFERER'])
        return redirect(reverse('main:home'))

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('main:home'))

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main/login_register.html', {'action':'register', 'form':UserCreationForm()})
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect(reverse('main:home'))
        else:
            messages.error(request, 'An error occurred during registration')

class HomeView(View):
    template_name = 'main/home.html'
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') else ''
        rooms = Room.objects.filter(
            Q(topic__name__icontains = q) | 
            Q(name__icontains = q) |
            Q(description__icontains = q) |
            Q(host__username__icontains = q)
        )
        context = {'rooms': rooms, 'room_count':rooms.count(), 'topics':Topic.objects.all()}
        return render(request, 'main/home.html', context)


def contact(request):
    return render(request, 'main/contact.html', {})


# class createRoom2(CreateView):
#     template_name = 'main/room_form.html'
#     form_class = RoomForm
#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return super().form_valid(form)
#     def get_success_url(self):
#         return reverse('main:home')
 


class createRoom(LoginRequiredMixin, View):
    def get(self, request):
        context = {'form':RoomForm()}
        return render(request, 'main/room_form.html', context)
    def post(self, request, *args, **kwargs):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:home'))

# class updateRoom2(UpdateView):
#     template_name = 'main/room_form.html'
#     form_class = RoomForm
#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return super().form_valid(form)
#     def get_object(self):
#         return get_object_or_404(Room, id = self.kwargs.get('pk'))
#     def get_success_url(self):
#         return reverse('main:home')

class updateRoom(LoginRequiredMixin, View):
    def get(self, request, pk):
        room = get_object_or_404(Room, id = self.kwargs.get('pk'))
        if request.user != room.host:
            return HttpResponse(f"You are not allowed to edit '<i>{room}</i>' , it belongs to @{room.host.username}")

        form = RoomForm(instance=room)
        return render(request, 'main/room_form.html', {'form':form})
    def post(self, request, pk): 
        room = get_object_or_404(Room, id = self.kwargs.get('pk'))
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:home'))

class deleteRoom(LoginRequiredMixin, View):
    template_name = 'main/delete_form.html'
    def get(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        if request.user != room.host:
            return HttpResponse(f"You are not allowed to delete '<i>{room}</i>' , it belongs to @{room.host.username}")
        return render(request, 'main/delete_form.html', {'object':room})
    def post(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        room.delete()
        return redirect(reverse('main:home'))

