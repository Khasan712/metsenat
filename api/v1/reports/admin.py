from typing import List
from django.contrib import admin

# Register your models here.

from api.v1.reports.models import (
    SponsorCash,
    SponsorInvets,
    SponsorStudent
)

@admin.register(SponsorCash)
class SponsorCashAdmin(admin.ModelAdmin):
    list_display = ('id', 'sponsor', 'uzs_money', 'usd_money', 'status', 'created_at')
    
    
@admin.register(SponsorInvets)
class SponsorInvetsAdmin(admin.ModelAdmin):
    list_display = ('id', 'sponsorCash', 'priceType', 'money', 'is_active', 'created_at')
    
    
@admin.register(SponsorStudent)
class SponsorStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'sponsor', 'student', 'money', 'priceType', 'created_at', 'is_active')
    
    
    
    
