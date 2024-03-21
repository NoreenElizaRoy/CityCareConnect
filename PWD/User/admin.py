from django.contrib import admin

# Register your models here.
from .models import Official,CustomUser

admin.site.register(Official)
admin.site.register(CustomUser)