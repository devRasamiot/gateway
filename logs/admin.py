from django.contrib import admin
from .models import  LogData, LiveData

# Register your models here.
# admin.site.register(BoardProperty)
admin.site.register(LogData)
admin.site.register(LiveData)
