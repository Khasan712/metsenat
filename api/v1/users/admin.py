from django.contrib import admin

# Register your models here.

from api.v1.users.models import (
    User,
    ApplicationForSponsor
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phone_number', 'is_active', 'is_deleted')


@admin.register(ApplicationForSponsor)
class ApplicationForSponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phoneNumber', 'is_active', 'is_deleted')
    
    
    
