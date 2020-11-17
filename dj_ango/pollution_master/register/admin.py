from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
# from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser


# admin.site.register(User)

admin.site.register(Profile)
