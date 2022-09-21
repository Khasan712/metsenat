from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser
from api.v1.reports.models import SponsorCash, SponsorStudent
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.functions import Coalesce
from django.db.models import Count, Q, Sum, Avg, DecimalField, F
from django.core.validators import FileExtensionValidator
from api.v1.users.enums import (
    IOHE,
    Gender,
    Regions,
    StudentType,
    UserRoles,
)
from api.v1.users.managers import (
    AdminManager,
    MyAccountManager,
    SponsorManager,
    # StudentsManager,
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
    region = models.CharField(max_length=30, choices=Regions.choices())
    # studentType = models.CharField(max_length=8, choices=StudentType.choices(), blank=True, null=True)
    # iohe = models.CharField(max_length=4, choices=IOHE.choices(), blank=True, null=True)
    # studentContract = models.FloatField(default=0)
    email = models.EmailField(max_length=50, blank=True, null=True)
    
    physicalPerson = models.BooleanField(default=False)
    legalEntity = models.BooleanField(default=False)
    
    gender = models.CharField(max_length=5, choices=Gender.choices(), blank=True, null=True)
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
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    
    
    

class Admin(User):
    
    objects = AdminManager()

    class Meta:
        proxy = True
        
class Sponsor(User):
    
    objects = SponsorManager()

    class Meta:
        proxy = True
        
        
class Student(models.Model):
    phone_number = models.CharField(max_length=55, unique=True)
    flf = models.CharField(verbose_name='Name', max_length=150)
    # role = models.CharField(max_length=20, choices=UserRoles.choices())
    region = models.CharField(max_length=30, choices=Regions.choices())
    studentType = models.CharField(max_length=8, choices=StudentType.choices(), blank=True, null=True)
    iohe = models.CharField(max_length=4, choices=IOHE.choices(), blank=True, null=True)
    studentContract = models.FloatField(default=0)
    email = models.EmailField(max_length=50, blank=True, null=True)

    gender = models.CharField(max_length=5, choices=Gender.choices(), blank=True, null=True)
    avatar = models.ImageField(
        upload_to=upload_location_avatar,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'svg']), validate_size_image],
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    @property
    def get_sum(self):
        studentSum = SponsorStudent.objects.select_related('sponsor',).filter(
            student_id=self.id, is_active=True, is_deleted=False
        ).aggregate(foo=Coalesce(Sum('money'), 0.0))['foo']
        return studentSum
    
    @property
    def get_sponsors(self):
        sponsors = SponsorStudent.objects.select_related('sponsor',).filter(student_id=self.id, is_active=True, is_deleted=False)
        sponsors_list = []
        for sponsor in sponsors:
            data = {
                'flf': sponsor.sponsor.sponsor.flf,
                'money': sponsor.money,
                'priceType': sponsor.priceType,
            }
            sponsors_list.append(data)
        return sponsors_list
            
    @property
    def get_sponsors_list(self):
        sponsors = SponsorCash.objects.select_related('sponsor',).filter(sponsorCash__student_id=self.id)
        sponsor_list = []
        for sponsor in sponsors:
            money = SponsorStudent.objects.select_related('sponsor', 'student').filter(
                sponsor_id=sponsor.id, student_id=self.id
            ).aggregate(
                foo=Coalesce(Sum('money'), 0.0)
            )['foo']
            
            data = {
                'flf':sponsor.sponsor.flf,
                'money': money,
                'priceType': sponsor.priceType,
            }
            sponsor_list.append(data)
        return sponsor_list
    
    

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
        validators=[phone_regex_validator], max_length=15
    )
    money = models.FloatField(default=0)
    companyName = models.CharField(max_length=150, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        if self.physicalPerson is True:
            return f"{self.flf}: {self.physicalPerson} - {self.money}"
        else:
            return f"{self.flf}: {self.legalEntity} - {self.money}"