from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'cedula', 'first_name', 'last_name', 'is_staff')


admin.site.register(User, UserAdmin)