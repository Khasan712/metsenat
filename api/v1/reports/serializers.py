from pyexpat import model
from api.v1.users.models import Sponsor
from rest_framework import serializers
from django.db import models, transaction

from api.v1.reports.models import (
    SponsorCash,
    SponsorInvets,
    SponsorStudent,
)



# class BecomeSponsorListSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = BecomeSponsor
#         exclude = ('get_sponsor_flf', 'get_sponsor_phoneNumber', 'money', 'get_expences_money', '')


class SponsorInvestSerializer(serializers.ModelSerializer):
    sponsor_id = serializers.IntegerField(required=True)
    class Meta:
        model = SponsorInvets
        fields = ('priceType', 'money', 'sponsor_id')
        
    def save(self,  **kwargs):
        sponsor_id = self.validated_data.get("sponsor_id")
        money = self.validated_data.get("money")
        priceType = self.validated_data.get("priceType")
        sponsor = Sponsor.objects.filter(id=sponsor_id, is_active=True, is_deleted=False).first()
        if not sponsor:
            raise serializers.ValidationError({"error": "Sponsor not found."})
        with transaction.atomic():
            sponsorCash, created = SponsorCash.objects.get_or_create(sponsor_id=sponsor_id)
            sponsorInvest = SponsorInvets(
                sponsorCash_id=sponsorCash.id,
                money=money,
                priceType=priceType
            )
            sponsorInvest.save()
            if priceType == 'UZS':
                sponsorCash.uzs_money += money
            else:
                sponsorCash.usd_money += money
            sponsorCash.save()
        return sponsorInvest
        
class AddSponsorToStudentSerializer(serializers.ModelSerializer):
    sponsor_id = serializers.IntegerField(required=True)
    money = serializers.FloatField(required=True)
    priceType = serializers.CharField(required=True)
    
    class Meta:
        model = SponsorStudent
        fields = ('student', 'priceType', 'sponsor_id', 'money')

    def save(self, **kwargs):
        sponsor_id = self.validated_data.get("sponsor_id")
        money = self.validated_data.get("money")
        priceType = self.validated_data.get("priceType")
        student = self.validated_data.get("student")
        sponsor = Sponsor.objects.filter(id=sponsor_id, is_active=True, is_deleted=False).first()
        sponsorCash = SponsorCash.objects.filter(sponsor_id=sponsor_id).first()
        if not sponsor:
            raise serializers.ValidationError({"error": "Sponsor not found."})
        if not sponsorCash:
            raise serializers.ValidationError({"error": "Sponsor has not cash."})
        if priceType == 'UZS':
            if sponsorCash.uzs_money < money:
                raise serializers.ValidationError({"error": "Sponsor not enough UZS."})
        if priceType == 'USD':
            if sponsorCash.usd_money < money:
                raise serializers.ValidationError({"error": "Sponsor not enough UZS."})
        with transaction.atomic():
            addSponsorToStudent = SponsorStudent(
                sponsor_id=sponsorCash.id,
                student_id=student.id,
                money=money,
                priceType=priceType,
            )
            if priceType == 'UZS':
                sponsorCash.uzs_money -= money
            else:
                sponsorCash.usd_money -= money
            addSponsorToStudent.save()
            sponsorCash.save()
        return addSponsorToStudent

class SponsorsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorCash
        fields = (
            'id', 'get_sponsor_flf',
            'get_sponsor_phoneNumber',
            'uzs_money', 'usd_money',
            'get_expences_money_uzs',
            'get_expences_money_usd',
            'created_at',
            'status'
            )
                
                 
            