from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')


admin.site.register(User, UserAdmin)
