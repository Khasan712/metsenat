from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import FileExtensionValidator
from api.v1.users.enums import (
    Gender,
    UserRoles,
)
from api.v1.users.managers import (
    MyAccountManager,
)
from api.v1.users.services import (
    upload_location_avatar,
    validate_size_image,
)

# Create your models here.


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=55, unique=True)
    flf = models.CharField(verbose_name='Name', max_length=150)
    role = models.CharField(max_length=20, choices=UserRoles.choices())
    email = models.EmailField(max_length=50, blank=True, null=True)
    
    physicalPerson = models.BooleanField(default=False)
    legalEntity = models.BooleanField(default=False)
    
    gender = models.CharField(max_length=5, choices=Gender.choices(), default=Gender.man.value)
    avatar = models.ImageField(
        upload_to=upload_location_avatar,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']), validate_size_image],
        blank=True,
        null=True,
    )
    
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    last_login = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['flf', 'role']
    
    objects = MyAccountManager()

    def __str__(self):
        return self.flf

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
            
    # def save(self, *args, **kwargs):
    #     last_user_id = User.objects.last()
    #     self.phone_number = f'{last_user_id.id}|{self.phone_number}'
    #     super().save(*args, **kwargs)




class ApplicationForSponsor(models.Model):
    physicalPerson = models.BooleanField(default=False)
    legalEntity = models.BooleanField(default=False)
    flf = models.CharField(verbose_name='Name', max_length=150)
    phone_regex_validator = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+998991234567'. "
        "Up to 15 digits allowed.",
    )
    phoneNumber = models.CharField(
        validators=[phone_regex_validator], max_length=15, unique=True
    )
    money = models.FloatField(default=0)
    companyName = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        if self.physicalPerson is True:
            return f"{self.flf}: {self.physicalPerson} - {self.money}"
        else:
            return f"{self.flf}: {self.legalEntity} - {self.money}"