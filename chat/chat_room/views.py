from django.shortcuts import render ,redirect
from django.db.models import Q
from .models import Room ,Topic ,Message ,ProfileUser
from django.http import HttpResponse
from django.contrib.auth import authenticate ,login ,logout
from .forms import CreateRoom ,UpdateRoom ,ProfileUserForm
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
# Create your views here.

def loginpage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("rooms")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User dos not exist")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successfully")
            return redirect("rooms")
        else:
            messages.error(request,"Username OR Password does not exit")
    return render(request,"room/login_register.html",{'page':page})

def registerpage(request):
    page = "register"
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            messages.success(request,"Register is Successfully")
            p = ProfileUser.objects.get_or_create(user=user)
            return redirect("rooms")
        else:
            messages.error(request,"form is not valid!!!")
    else:
        form = UserCreationForm()
    return render(request,"room/login_register.html",{'page':page,'form':form})

@login_required(login_url="login_register")
def rooms(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    room = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)|
        Q(name__icontains=q)
        )
    
    topics = Topic.objects.all()
    room_count = Room.objects.filter(participants=request.user).count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by("-created","-updated")
    context = {
        'rooms':room,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_message,
        'q':q,
    }
    return render(request,"room/room.html",context)

def caht_rooms(request,pk):
    rooms = Room.objects.get(id=pk)
    room_messages = rooms.message_set.all()
    participants = rooms.participants.all()
    number = rooms.participants.count()

    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body")
        message = Message.objects.create(
            user = request.user,
            room=rooms,
            body = body
        )
        return JsonResponse({
            'id': message.id,
            'user': message.user.username,
            'body': message.body,
        })

    return render(request,"room/chat_room.html",{'room':rooms,'room_messages':room_messages,'participants':participants,'member':number})

@login_required(login_url="login_register")
def updateimage(request,pk):
    get_user = ProfileUser.objects.get(user__id=pk)
    if request.method == "POST":
        form = ProfileUserForm(request.POST,request.FILES,instance=get_user)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect("profile",pk=pk)
        else:
            messages.error(request,"form is not valid!!!")
    else:
        form = ProfileUserForm(instance=get_user)
    return render(request,"room/update_image.html",{'form':form})

@login_required(login_url="login_register")
def profileuser(request,pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    topics = Topic.objects.all()
    image_profile = ProfileUser.objects.get(user=user)
    context={"user":user,"room":room,'topic':topics,'image':image_profile}
    return render(request,"room/profile.html",context)

@require_POST
def add_user(request,pk):
    get_user = request.user
    get_room = Room.objects.get(id=pk)
    if get_user and get_room:
        try:
            get_room.participants.add(request.user)
            messages.success(request,f"{get_user} your add in {get_room}")
            return redirect("chat_room",pk=pk)
        except:
            messages.error(request,"error")
    else:
        messages.error(request,"user or room is not find!!!")

@login_required(login_url="login_register")
def create_room(request):
    if request.method == "POST":
        form = CreateRoom(request.POST,files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.host = request.user
            user.save()
            user.participants.add(request.user)
            return redirect("chat_room",pk=user.id)
        else:
            pass
    else:
        form = CreateRoom()
    return render(request,"room/form_room.html",{'form':form})

@login_required(login_url="login_register")
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = UpdateRoom(instance=room)
    if request.method == "POST":
        form = UpdateRoom(request.POST,instance=room,files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.host = request.user
            user.save()
            return redirect("chat_room", pk=pk)
        else:
            pass
    else:
        form = UpdateRoom(instance=room)
    return render(request,"room/update_room.html",{'form':form,'room':room})



@login_required(login_url="login_register")
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    room.delete()
    return redirect("rooms")

def logoutuser(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect("rooms")

@login_required(login_url="login_register")
def deletemessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("Your are not allowed here")
        
    
    if request.method == "POST":
        room_id = message.room.id
        message.delete()
        return redirect("chat_room",pk=room_id)
    return render(request,"room/delete.html",{"obj":message})



@require_POST
def leave_user(request,pk):
    get_user = request.user
    get_room = Room.objects.get(id=pk)
    if get_user and get_room:
        try:
            get_room.participants.remove(request.user)
            messages.success(request,f"{get_user} your leave in {get_room}")
            return redirect("rooms")
        except:
            messages.error(request,"error")
    else:
        messages.error(request,"user or room is not find!!!")