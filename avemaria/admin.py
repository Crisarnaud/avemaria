from django.contrib import admin

from .models import Book, UserProfileInfo, User
from django.contrib import admin

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Book)