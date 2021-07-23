from django.urls import path
from main.views import *

from django.conf.urls.static import static
from django.conf import settings
app_name = 'main'

urlpatterns = [
    path('', home_view, name="home_page"),
    path('register/', regiser_view, name="register"),
    path('notfound/', notfound_view, name="notfound"),
    path('addroom/', addroom_view, name="addroom"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('roomdetail/<catagory>/', roomdetail_view, name="roomdetail"),
    path('singleview/<singleuser>/', single_view, name="singleview"),
    path('roombooking/<slug>/', roombooking_view, name="roombooking"),
    path('services/', services_view, name="services"),
    path('serviceupdate/<service_id>/', serviceupdate_view, name="serviceupdate"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)