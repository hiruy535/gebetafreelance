from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from main.forms import *
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.files import File

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
from chatall.models import Thread, ChatMessage

def get_search_query(query=None):
    queryset= []
    queries = query.split(" ")
    for q in queries:
        if q != "":
            searchs = Room.objects.filter(
                Q(catagory__categoryname__icontains=q)).distinct()
            

            for post in searchs:
                print(post)
                queryset.append(post)
    return list(set(queryset))
def get_other_users(request):
    thread = Thread.objects.all()
    other_users = []
    mythread = []
    for t in thread:
        if request.user == t.first:
            mythread.append(t)
        elif request.user == t.second:
            mythread.append(t)
    for my in mythread:
        if request.user != my.first:
            other_users.append(my.first.username)
        if request.user != my.second:
            other_users.append(my.second.username)
    if len(other_users) != 0:
        return other_users[0]
    else:
        return other_users
def home_view(request):
    #Thread.objects.get_message()
        
    context = {}
    search = request.POST.get('search')
    if search:
        #users = Room.objects.filter(catagory__categoryname=search.lower())
        #print(users)
        users = get_search_query(search)
        catagorys = Category.objects.filter(~Q(categoryname__icontains=search.lower()))

        if users:
            context = {'ids':search,'users':users,'catagorys':catagorys}
            return render(request,'main/roomdetail.html',context)

    searchRoom = Category.objects.all()

    if request.user.is_authenticated:
        form = CompleteUserProfileForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            form = CompleteUserProfileForm()
           
    useraddress = request.POST.get('firstname')
    #searchRoom = Room.objects.filter(roomname=search)
    if searchRoom:
        room_list = searchRoom
    else:
        room_list =Room.objects.all()
    paginator = Paginator(room_list,4)

    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        rooms = paginator.page(page)
    except(EmptyPage, InvalidPage):
        rooms = paginator.page(paginator.num_pages)

    star = request.GET.get('starRateValue')
    context['rooms'] = rooms
    #context['star'] = star
    context['useraddress'] = useraddress
    context['catagorys'] = Category.objects.all()
    context['other_users'] = get_other_users(request)



    return render(request,'main/home.html',context)




def addroom_view(request):
    rate = request.POST.get('starRate')
    item_id = request.POST.get('item_id')
    #price = AddPriceBasic()
    if rate:
        rated = False
        response_data = {}
        response_data['starRate'] = rate + " hira"
        response_data['item_id'] = "item id: " + item_id
        user = request.user
        item = Room.objects.get(id=item_id)
        ra = Rate.objects.get_or_new(user,item.roomname)
        rt = Rate.objects.all()

        #for i in ite:
            #print(i.rate_amount)
        for rat in rt:
            ratEX = Rate.objects.get_or_new(rat.user,rat.room.roomname)
            if ra == ratEX:
                rated = True
                rat.rate_amount = rate
                rat.save(update_fields=['rate_amount'])
                ite = Rate.objects.set_total(item)
                return JsonResponse(response_data)

        if rated == False :
            rateSave = Rate.objects.create()
            rateSave.user = user
            rateSave.room = item
            rateSave.rate_amount = rate
            rateSave.save()
            ite = Rate.objects.set_total(item)
            return JsonResponse(response_data)
        #print(ra)

        context['other_users'] = get_other_users(request)
    else:
        context = {}
        #form = AddRoomForm(request.POST, request.FILES)
        form = AddServiceForm(request.POST, request.FILES)
        if request.POST:
            catagory = request.POST.get('catagory')
            if catagory != 'Catagory List':
                catagorys = Category.objects.get(categoryname=catagory)
                if catagorys:
                    if form.is_valid():
                        room = form.save(commit=False)
                        room.catagory = catagorys
                        room.room_user= request.user

                        price = Price.objects.create()
                        basic_price_title = request.POST.get('basic_price_title')
                        basic_price = request.POST.get('basic_price')
                        basic_price_discription = request.POST.get('basic_price_discription')
                        basic_price_delivery = request.POST.get('basic_price_delivery')
                        
                        price.price_title = basic_price_title
                        price.price_number = basic_price
                        price.price_delivery = basic_price_delivery
                        price.price_description = basic_price_discription
                        
                        price.save()

                        pricebasic = PriceBasic.objects.create()
                        pricebasic.price = price
                        pricebasic.save()

                        pricestandard = Price.objects.create()
                        basic_price_title = request.POST.get('standard_price_title')
                        basic_price = request.POST.get('standard_price')
                        basic_price_discription = request.POST.get('standard_price_discription')
                        basic_price_delivery = request.POST.get('standard_price_delivery')
                        
                        pricestandard.price_title = basic_price_title
                        pricestandard.price_number = basic_price
                        pricestandard.price_delivery = basic_price_delivery
                        pricestandard.price_description = basic_price_discription
                        
                        pricestandard.save()

                        standard = PriceStandard.objects.create()
                        standard.price = pricestandard
                        standard.save()


                        pricepremium = Price.objects.create()
                        basic_price_title = request.POST.get('premium_price_title')
                        basic_price = request.POST.get('premium_price')
                        basic_price_discription = request.POST.get('premium_price_discription')
                        basic_price_delivery = request.POST.get('premium_price_delivery')
                        
                        pricepremium.price_title = basic_price_title
                        pricepremium.price_number = basic_price
                        pricepremium.price_delivery = basic_price_delivery
                        pricepremium.price_description = basic_price_discription
                        
                        pricepremium.save()

                        premium = PricePremium.objects.create()
                        premium.price = pricepremium
                        premium.save()

                        room.pricebasic = pricebasic 
                        room.pricepremium = premium
                        room.pricestandard = standard
                        #return redirect('main:home_page')
                        form.save()
                        form = AddServiceForm()
            else:
                context['catagory_selection_error'] = "Please Select A Catagory"
       
        context['allroom'] = form
        context['allusers'] = Account.objects.all()
        context['catagorys'] = Category.objects.all()
        context['other_users'] = get_other_users(request)
        return render(request,'main/addroom.html',context)

def regiser_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        genderValue = request.POST.get('genderValue')
        print(genderValue) 
        if form.is_valid():
            fr = form.save(commit=False)
            if genderValue == 'Male':
                #with open('static/images/dummy-profile-image-male.png', 'rb') as f:
                    #data = f.read()
                    #print(data,genderValue)
                fr.profile_image = 'dummy-profile-image-male.png'

            elif genderValue == 'Female':
                fr.profile_image = 'dummy-profile-image-Female.jpg'  
            fr.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account:
                login(request, account)
                return redirect('main:home_page')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request,'main/register.html', context)

def login_view(request):
    context = {}
    user = request.user
    email = 'email'
    if user.is_authenticated:
        return redirect('main:home_page')
    if request.POST:
        form = AccountAuthonticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('main:home_page')

    else:
        form = AccountAuthonticationForm()

    context['login_form'] = form
    context['login'] = email
    return render(request,'main/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('main:home_page')

def single_view(request,singleuser):
    users = Room.objects.get(id=singleuser)
    if request.POST:
        comments = request.POST.get('addComment')
        if request.user.is_authenticated:
            if comments:
                comment = Comment.objects.create() 
                comment.user = request.user
                comment.room = users
                comment.comment = comments
                comment.save()
                comments = ''
    Comments  = Comment.objects.filter(room=users)
    paginator = Paginator(Comments,5)

    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        Comments = paginator.page(page)
    except(EmptyPage, InvalidPage):
        Comments = paginator.page(paginator.num_pages)

    all_images = []
    if users.roomimage1:
        all_images.append(users.roomimage1.url)
    else:
        all_images.append(users.roomimage.url)
    if users.roomimage2:    
        all_images.append(users.roomimage2.url)
    if users.roomimage3:
        all_images.append(users.roomimage3.url)
    if users.roomimage4:
        all_images.append(users.roomimage4.url)

    servicess = Room.objects.filter(catagory__categoryname=users.catagory.categoryname).order_by('-total_rate')
    services = servicess.filter(~Q(id=singleuser))
    catagorys = Category.objects.filter(~Q(categoryname=singleuser))
    context = {'Comments':Comments,'users':users,'catagorys':catagorys,
               'coms':Comment.objects.filter(room=users), 'other_users':get_other_users(request)
               ,'services':services, 'all_images':all_images}
    return render(request,'main/singleview.html',context)

def roomdetail_view(request,catagory):
    users = Room.objects.filter(catagory__categoryname=catagory).order_by('-total_rate')
    catagorys = Category.objects.filter(~Q(categoryname=catagory))
    context = {'ids':catagory,'users':users,'catagorys':catagorys,'other_users':get_other_users(request)}
    return render(request,'main/roomdetail.html',context)


def roombooking_view(request, slug):
    #data = json.loads(request.data)
    room_list = Room.objects.filter(~Q(id=slug))

    paginator = Paginator(room_list,3)

    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1

    try:
        rooms = paginator.page(page)
    except(EmptyPage, InvalidPage):
        rooms = paginator.page(paginator.num_pages)

    context = {}
    context['rooms'] = rooms
    context['bookroom'] = Room.objects.get(id=slug)
    #return JsonResponse('here we go', safe=False)
    return render(request,'main/roombooking.html',context)

def searchRoom_view(request,slug):
    context = {}
    search = request.GET.get('search')
    context['serachedrooms'] = Room.objects.filter(roomname=search)
    return render(request,'main/home.html',context)
def services_view(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        context['services'] = Room.objects.filter(room_user=user)
        context['other_users'] = get_other_users(request)
    return render(request,'main/services.html',context)

def serviceupdate_view(request, service_id):
    context = {}
    if request.user.is_authenticated:
        service_id = service_id
        service = Room.objects.get(id=service_id)
        if request.POST:

            form = UpdateServiceForm(request.POST, request.FILES,instance=service)
            #service.roomname        = request.POST.get('roomname')
            #service.car_price       = request.POST.get('car_price')
            #service.car_description = request.POST.get('car_description')
            catagory                = Category.objects.get(categoryname=request.POST.get('catagory'))
            service.catagory        = catagory
            #service.roomimage       = request.POST.get('roomimage')
            #print(request.POST.get('roomimage'))
            #if form.is_valid():
            #print(service)
            #room = form.save(commit=False)
                #room.catagory = catagorys
                #room.room_user= request.user
            #room.save()
            form.save()
            service.save()
            #form.save()
            #form = AddServiceForm()

            #else:
                #print(form)

            #service.rate_amount = rate
            #service.save(update_fields=['rate_amount'])
        context['service'] = service
        context['catagorys'] = Category.objects.all()
        context['other_users'] = get_other_users(request)
    return render(request,'main/serviceupdate.html',context)
def notfound_view(request):
    context = {}
    context['other_users'] = get_other_users(request)
    return render(request,'main/notfound.html',context)