
from django.urls import path

from . import views
from .views import ThreadView
app_name = 'chat'

urlpatterns = [
    
    path('<str:room_name>/', ThreadView.as_view(), name='room'),
]
