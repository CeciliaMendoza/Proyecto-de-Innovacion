from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import User

class User_admin(admin.ModelAdmin):
    readonly_fields=("created",)


admin.site.register(User, User_admin)