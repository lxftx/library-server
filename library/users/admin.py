from django.contrib import admin
from users.models import UserLogLogin

# Register your models here.

@admin.register(UserLogLogin)
class UserLogLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address')
