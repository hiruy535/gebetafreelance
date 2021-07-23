from django.shortcuts import render
from chatall.models import Thread, ChatMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView
from .forms import ComposeForm
from main.models import *


def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):   
    chatmessage = ChatMessage.objects.all()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chatmessage': chatmessage,
    })
class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/room.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user.username)

    def get_object(self):
        other_username  = self.kwargs.get("room_name")
        if self.request.user.username != other_username:
            obj, created  = Thread.objects.get_or_new(self.request.user, other_username)
            if obj == None:
                raise Http404
            return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        catagorys = Category.objects.all()
        context['catagorys'] = catagorys
        thread = Thread.objects.all()
        other_users = []
        mythread = []
        for t in thread:
            if self.request.user == t.first:
                mythread.append(t)
            elif self.request.user == t.second:
                mythread.append(t)
        for my in mythread:
            if self.request.user != my.first:
                other_users.append(my.first)
            if self.request.user != my.second:
                other_users.append(my.second)
        allchats = ChatMessage.objects.all()
        mychat = []
        other_username = self.kwargs.get("room_name")
        other_user = []
        for my in mythread:
            if self.request.user.username == my.first.username and other_username == my.second.username:
                print(my.first.username, my.second.username)
                other_user.append(my)
            elif self.request.user.username == my.second.username and other_username == my.first.username:
                print(my.first.username, my.second.username)
                other_user.append(my)
            
        
        allchats = ChatMessage.objects.all()
        for allchat in allchats:
            if allchat.thread == other_user[0]:
                mychat.append(allchat)
        
        context['other_users'] = mythread
        context['mychat'] = mychat
        context['chat_user'] = other_username
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user.username
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)
