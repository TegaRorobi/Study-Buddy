from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import *
from .forms import *
from django.urls import reverse



# Create your views here.
class HomeView(View):
    template_name = 'main/home.html'
    def get(self, request):
        q = request.GET.get('q')
        context = {'rooms':Room.objects.filter(topic__name=q), 'topics':Topic.objects.all()}
        return render(request, 'main/home.html', context)




def contact(request):
    return render(request, 'main/contact.html', {})


class createRoom(CreateView):
    template_name = 'main/room_form.html'
    form_class = RoomForm
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('main:home')
 

class createRoom2(View):
    def get(self, request):
        context = {'form':RoomForm()}
        return render(request, 'main/room_form.html', context)
    def post(self, request, *args, **kwargs):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:home'))

class updateRoom(UpdateView):
    template_name = 'main/room_form.html'
    form_class = RoomForm
    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
    def get_object(self):
        return get_object_or_404(Room, id = self.kwargs.get('pk'))
    def get_success_url(self):
        return reverse('main:home')

class updateRoom2(View):
    def get(self, request, pk):
        room = get_object_or_404(Room, id = self.kwargs.get('pk'))
        form = RoomForm(instance=room)
        return render(request, 'main/room_form.html', {'form':form})
    def post(self, request, pk): 
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:home'))

class deleteRoom(View):
    template_name = 'main/delete_form.html'
    def get(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        return render(request, 'main/delete_form.html', {'object':room})
    def post(self, request, pk):
        room = get_object_or_404(Room, id=pk)
        room.delete()
        return redirect(reverse('main:home'))