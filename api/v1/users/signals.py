from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from api.v1.users.models import (
    Sponsor
)
from api.v1.reports.models import (
    BecomeSponsor
)
 
@receiver(post_save, sender=Sponsor)
def create_history_company(sender, instance, created, **kwargs):
    if created:
        BecomeSponsor.objects.create(sponsor=instance, money=instance.money)