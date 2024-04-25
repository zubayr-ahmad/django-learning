from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm  
from .models import Message
# Create your views here.

# rooms = [
#     {"id":1, "name":"Lets learn Python"},
#     {"id":2, "name":"Design with me"},
#     {"id":3, "name":"Frontend developers"},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)    # creates the session inside the database and inside the browser
            return redirect("home")
        else:
            messages.error(request, "Username OR Password is not correct.")
    context = {'page':page}
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    form = UserCreationForm()
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)      # this will create the object of the model based on form data (and returns) but does not save it to database yet
            user.username = user.username.lower()
            user.save()
            login(request, user)    # logging in the newly created user as well
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
    return render(request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q ) |
        Q(name__icontains = q)  |
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()      # can also use len(rooms) but it is relatively slow
    context = {"rooms" : rooms, "topics":topics, "room_count":room_count}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.message_set.all().order_by('-created')   # message = Message -> model name
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')     # 'body' is the name inside the input
        )
        room.participants.add(request.user)     # adding the logged in user in the room when he sends the message if not already entered
        return redirect('room', pk=room.id)
    context = {"room":room, 'room_messages':messages, 'participants':participants}
    return render(request, "base/room.html", context=context)

@login_required(login_url='login')      # if the user is not logged in then we will redirect to login
def createRoom(request):
    form = RoomForm
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        
    context = {'form':form}
    return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host :
        return HttpResponse("You are not allowed to update the room of someone else!!")
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {'form':form}
    return render(request, "base/room_form.html", context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host :
        return HttpResponse("You are not allowed to update the room of someone else!!")
    
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj":room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user :
        return HttpResponse("You cannot delete other's message")
    
    if request.method == "POST":
        message.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj":message})