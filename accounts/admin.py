from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Profile Info', {'fields': ('user_type', 'profile_picture', 'bio', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Profile Info', {'fields': ('user_type', 'profile_picture', 'bio', 'phone_number')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
from django.contrib import admin

# Register your models here.
