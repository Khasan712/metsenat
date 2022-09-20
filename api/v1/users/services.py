from django.core.exceptions import ValidationError
from datetime import datetime

from . import models



def upload_location_avatar(instance, file):
    """
    Faylga joylashgan address | format: (media)/userID/avatars/role/first_name-last_name/
    """
    return f'{instance.id}/avatars/{instance.role}/{instance}/{file}'


def validate_size_image(file_in_obj):
    """
    Rasm hajmini tekshirish
    """

    size_limit = 2
    if file_in_obj.size > size_limit * 1024 * 1024:
        raise ValidationError(f'maximum file size: {size_limit}mb')

    

def phoneNumber_not_in_database(id, phone_number):
    """
    phone number bazada takrorlanmasligini tekshirish
    """
    phone_number = str(id) + '|' + str(phone_number)
    
    try:
        
        user = models.User.objects.get(phone_number=phone_number)
        return False
        
    except:
        
        return True