from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from main.forms import *
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json


def home_view(request):
    context = {}
    search = request.GET.get('search')
    searchRoom = Room.objects.filter(roomname=search)
    if searchRoom:
        room_list = searchRoom
    else:
        room_list =Room.objects.all()
    paginator = Paginator(room_list,6)

    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        rooms = paginator.page(page)
    except(EmptyPage, InvalidPage):
        rooms = paginator.page(paginator.num_pages)
    context['rooms'] = rooms
    context = {
        "first_name": "Anjaneyulu",
        "last_name": "Batta",
        "address": "Hyderabad, India"
    }

    return render(request,'main/home.html',context)


def addroom_view(request):
    context = {}
    form = AddRoomForm(request.POST, request.FILES)
    if form.is_valid():
        room = form.save(commit=False)
        room.slug = Room.id
        form.save()
        form = AddRoomForm()
    context['allroom'] = form
    context['allusers'] = Account.objects.all()
    return render(request,'main/addroom.html',context)

def regiser_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home page')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request,'main/register.html', context)

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home page')
    if request.POST:
        form = AccountAuthonticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('home page')
    else:
        form = AccountAuthonticationForm()

    context['login_form'] = form
    return render(request,'main/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('home page')

def roomdetail_view(request):
    context = {}
    return render(request,'main/roomdetail.html',context)


def roombooking_view(request, slug):
    #data = json.loads(request.data)
    context = {}
    context['bookroom'] = Room.objects.get(id=slug)
    #return JsonResponse('here we go', safe=False)
    return render(request,'main/roombooking.html',context)

def searchRoom_view(request,slug):
    context = {}
    search = request.GET.get('search')
    context['serachedrooms'] = Room.objects.filter(roomname=search)
    return render(request,'main/home.html',context)
