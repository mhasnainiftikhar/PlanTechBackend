# main/admin.py
from django.contrib import admin
from .models import User, Plant, Notification, GrowthHistory

# Register your models here
admin.site.register(User)
admin.site.register(Plant)
admin.site.register(Notification)
admin.site.register(GrowthHistory)
