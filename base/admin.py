from django.contrib import admin

# Register your models here.
from .models import Room 
admin.site.register(Room)

from .models import Topic
admin.site.register(Topic)

from .models import Message 
admin.site.register(Message)