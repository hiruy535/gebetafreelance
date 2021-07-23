from django.contrib import admin
from .models import *

admin.site.register(Account)
admin.site.register(Room)
admin.site.register(BookRoom)
admin.site.register(Category)
admin.site.register(Rate)
admin.site.register(Comment)
admin.site.register(PriceBasic)
admin.site.register(PriceStandard)
admin.site.register(PricePremium)
admin.site.register(Price)