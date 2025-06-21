from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

