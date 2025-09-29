from django.contrib import admin
from .models import Room ,Topic ,Message ,ProfileUser
# Register your models here.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(ProfileUser)