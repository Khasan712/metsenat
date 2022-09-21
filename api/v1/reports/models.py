from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Count, Q, Sum, Avg, DecimalField, F
# from api.v1.users.models import (
#     # Sponsor,
#     # Student,
# )
from api.v1.reports.enums import (
    StatusSponsor,
    PriceType
)

# Create your models here.





class SponsorCash(models.Model):
    sponsor = models.OneToOneField('users.Sponsor', on_delete=models.PROTECT, related_name='sponsoring')
    uzs_money = models.FloatField(default=0)
    usd_money = models.FloatField(default=0)
    status = models.CharField(max_length=12, choices=StatusSponsor.choices(), default=StatusSponsor.new.value)
    # priceType = models.CharField(max_length=3, choices=PriceType.choices(), default=PriceType.UZS.value)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.sponsor.flf} - UZS:{self.uzs_money} USD:{self.usd_money}'
    
    @property
    def get_expences_money_uzs(self):
        sponsorStudents = SponsorStudent.objects.select_related('sponsor','student').filter(
            sponsor_id=self.id, priceType='UZS'
        ).aggregate(foo=Coalesce(Sum('money'), 0.00, output_field=DecimalField()))['foo']
        return sponsorStudents

    @property
    def get_expences_money_usd(self):
        sponsorStudents = SponsorStudent.objects.select_related('sponsor','student').filter(
            sponsor_id=self.id, priceType='USD'
        ).aggregate(foo=Coalesce(Sum('money'), 0.00, output_field=DecimalField()))['foo']
        return sponsorStudents
    
    @property
    def get_sponsor_flf(self):
        return f'{self.sponsor.flf}'
    
    @property
    def get_sponsor_phoneNumber(self):
        return f'{self.sponsor.phone_number}'


class SponsorInvets(models.Model):
    sponsorCash = models.ForeignKey(SponsorCash, on_delete=models.PROTECT)
    money = models.FloatField(default=0)
    priceType = models.CharField(max_length=3, choices=PriceType.choices(), default=PriceType.UZS.value)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.sponsorCash.sponsor.flf} - {self.money} data: {self.created_at}'
    

class SponsorStudent(models.Model):
    sponsor = models.ForeignKey(SponsorCash, on_delete=models.PROTECT, related_name='sponsorCash')
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT, related_name='sponsorStudent')
    money = models.FloatField(default=0)
    priceType = models.CharField(max_length=3, choices=PriceType.choices(), default=PriceType.UZS.value)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.student.flf} - {self.money}'
    
    