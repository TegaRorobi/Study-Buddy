from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Message, Room, User
from django.views.generic import *
from .forms import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('main:home'))
        return render(request, 'main/login-register.html', {'action':'login'})
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You have logged in successfully as {request.user}')
        else:
            messages.error(request, 'username or pasword does not exist')
        # print(request.META['HTTP_REFERER'])
        return redirect(reverse('main:home'))

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('main:home'))

class RegisterView(View):
    def get(self, request):
        return render(request, 'main/login-register.html', {'action':'register', 'form':MyUserCreationForm()})
    def post(self, request):
        print(request.POST)
        #! always remember to pass in request.FILES when submitting forms that have an Imagefield or any type of filefield
        # ! attached to them
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()
            login(request, user)
        else:
            messages.error(request, 'An error occured during registration')
        return redirect(reverse('main:home'))
        
class RoomView(View):
    def get(self, request, room_name):
        room = Room.objects.get(name=room_name)
        room_messages = room.messages.all()
        participants = room.participants.all()
        return render(request, 'main/room.html', {'room':room, 'room_messages':room_messages, 'participants':participants})
    def post(self, request, room_name):
        room = Room.objects.get(name=room_name)
        message = Message.objects.create(
            user=request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        messages.success(request, 'Your message has been posted successfully!')
        return self.get(request, room_name=room.name)

class HomeView(View):
    template_name = 'main/home.html'
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') else ''
        rooms = Room.objects.filter(Q(name__icontains=q) | Q(topic__name__icontains=q) | Q(host__username__icontains=q))[:6] 
        messages = Message.objects.filter(Q(room__in=rooms) | Q(room__topic__name__icontains=q))[:5]
        context = {'rooms': rooms, 'activity':messages, 'room_count':len(rooms), 'topics':Topic.objects.all()[:5]}
        return render(request, 'main/home.html', context)

class UserProfile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        rooms = user.owned_rooms.all()
        user_messages = user.messages.all()[:5]
        context = {'user':user, 'topics':Topic.objects.all()[:5], 'rooms':rooms, 'activity':user_messages}
        return render(request, 'main/profile.html', context)

class createRoom(LoginRequiredMixin, View):
    def get(self, request):
        context = {'form':RoomForm(), 'action':'create', 'topics':Topic.objects.all()}
        return render(request, 'main/cr_ud-room.html', context)
    def post(self, request, *args, **kwargs):
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'))
        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     new_room = form.save(commit=False)
        #     new_room.host = request.user
        #     new_room.save()
        return redirect(reverse('main:home'))

class updateRoom(LoginRequiredMixin, View):
    def get(self, request, pk):
        room = get_object_or_404(Room, id = self.kwargs.get('pk'))
        if request.user != room.host:
            return HttpResponse(f"You are not allowed to edit '<i>{room}</i>' , it belongs to @{room.host.username}")

        form = RoomForm(instance=room)
        
        return render(request, 'main/cr_ud-room.html', {'form':form, 'room':room, 'action':'update', 'topics':Topic.objects.all()})
    def post(self, request, pk): 
        room = get_object_or_404(Room, id = self.kwargs.get('pk'))
        topic, created = Topic.objects.get_or_create(name=request.POST.get('topic'))
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('main:view-room', room.name)

class deleteRoom(LoginRequiredMixin, View):
    template_name = 'main/delete_form.html'
    def get(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        if request.user != room.host:
            return HttpResponse(f"You are not allowed to delete '<i>{room}</i>' , it belongs to @{room.host.username}")
        return render(request, 'main/delete.html', {'object':room})
    def post(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        room.delete()
        return redirect(reverse('main:home'))

class deleteMessage(LoginRequiredMixin, View):
    template_name = 'main/delete_form.html'
    def get(self, request, pk):
        message = get_object_or_404(Message, id=pk)
        if request.user != message.user and request.user != message.room.host :
            return HttpResponse(f"You are not allowed to delete '<i>{message}</i>' , it belongs to @{message.user.username}")
        return render(request, 'main/delete.html', {'object':message})
    def post(self, request, pk):
        message = get_object_or_404(Message, id=pk)
        room = message.room
        if not room.messages.filter(user=message.user):
            room.participants.remove(message.user) 
        message.delete()
        return redirect(reverse('main:view-room', kwargs = {'room_name':room.name}))

class updateUser(LoginRequiredMixin, View):
    def get(self, request):
        form = MyUserUpdateForm(instance=request.user)
        print(form)
        return render(request, 'main/update-user.html', {'form':form})
    def post(self, request):
        form = MyUserUpdateForm(request.POST, request.FILES, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
        return redirect(reverse('main:user-profile', kwargs={'username':request.user.username}))
        
class TopicsView(View):
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') else ''
        topics = Topic.objects.filter(Q(name__icontains=q))
        return render(request, 'main/topics.html', {'topics':topics})

class ActivityView(View):
    def get(self, request):
        q = request.GET.get('q') if request.GET.get('q') else ''
        rooms = Room.objects.filter(Q(name__icontains=q) | Q(topic__name__icontains=q) | Q(host__username__icontains=q))[:6] 
        activity = Message.objects.filter(Q(room__in=rooms) | Q(room__topic__name__icontains=q))[:5]
        return render(request, 'main/activity.html', {'activity':activity})

"""
class createRoom2(CreateView):
    template_name = 'main/room_form.html'
    form_class = RoomForm
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('main:home')

class updateRoom2(UpdateView):
    template_name = 'main/create-room.html'
    form_class = RoomForm
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    def get_object(self):
        return get_object_or_404(Room, id = self.kwargs.get('pk'))
    def get_success_url(self):
        return reverse('main:home')
"""
