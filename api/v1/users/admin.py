from django.contrib import admin

# Register your models here.

from api.v1.users.models import (
    User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phone_number', 'is_active', 'is_deleted')
    