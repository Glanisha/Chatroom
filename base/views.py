from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room , Topic, Message
from .forms import RoomForm
from django.db.models import Q 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404



def loginpage(request):
    page="login"
    if request.user.is_authenticated:
        return redirect("base:home") 
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            return redirect("base:home") 
        else:
            print("Invalid username or password")
            messages.error(request, "Invalid username or password")
    return render(request, "base/login_register.html", {"page":page})



def logoutpage(request):
    logout(request)
    return redirect("base:loginpage")



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect("base:loginpage") 
        else:
            messages.error(request, "An error occurred during registration.")
    else:
        form = UserCreationForm()

    context = {"form": form, "page": "register"}
    return render(request, "base/login_register.html", context)
   


def home(request):
    q = request.GET.get('q')  
    if q:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    else:
        rooms = Room.objects.all()
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    if q:
        room_messages = Message.objects.filter(
            Q(room__topic__name__icontains=q)  
        ).order_by("-created")
    else:
        room_messages = Message.objects.all().order_by("-created")
    
    return render(request, "base/home.html", {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages
    })


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("base:room", pk=room.id)
    return render(request, "base/room.html", {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    })



@login_required(login_url="base:loginpage")
def createroom(request):
    form= RoomForm()
    if request.user!=room.host:
        return HttpResponse("invalid user")
    if request.method == "POST":
        form= RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("base:home")
    context={'form':form}
    return render(request,'base/roomform.html', context )



@login_required(login_url="base:loginpage")
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form= RoomForm(instance=room)
    if request.user!=room.host:
        return HttpResponse("invalid user")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("base:home")
    context={'form':form}
    return render(request,'base/updateform.html', context )



@login_required(login_url="base:loginpage")
def deleteroom(request, pk ): 
    room= Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("invalid user")
    if request.method=="POST":
        room.delete()
        return redirect("base:home")
    return render(request,'base/delete.html', {"object":room} )


@login_required(login_url="base:loginpage")
def deletemessage(request, pk ): 
    message= Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse("invalid user")
    if request.method=="POST":
        message.delete()
        return redirect("base:home")
    return render(request,'base/delete.html', {"object":message} )


def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    room_messages=user.message_set.all()
    context = {"user": user, "rooms":rooms, "room_messages":room_messages, "topics":topics}
    return render(request, "base/profile.html", context)