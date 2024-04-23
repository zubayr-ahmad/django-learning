from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message

# we are registering this model inside the admin so we can see it inside django admin panel.
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)