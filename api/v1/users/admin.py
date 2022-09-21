from django.contrib import admin

# Register your models here.

from api.v1.users.models import (
    User,
    ApplicationForSponsor,
    Admin,
    Sponsor,
    Student,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phone_number', 'is_active', 'is_deleted')
    

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phone_number', 'is_active', 'is_deleted')

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phone_number', 'is_active', 'is_deleted')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phone_number', 'is_active', 'is_deleted')

@admin.register(ApplicationForSponsor)
class ApplicationForSponsorAdmin(admin.ModelAdmin):
    list_display = ('id', 'flf', 'phoneNumber', 'is_active', 'is_deleted')
    
    
    
