from django.contrib.auth.models import BaseUserManager
from django.db.models import manager
from api.v1.users.enums import UserRoles

class MyAccountManager(BaseUserManager):
    
    def _create_user(self, phone_number, role, flf, password=None, **extra_fields):
        """check if user have set required fields"""
        if not phone_number:
            raise ValueError("user must have phone number")
        if not role:
            raise ValueError("user must have choose role")
        if not flf:
            raise ValueError("user must have firstName, lastName, father'sName")
        user = self.model(
            phone_number=phone_number,
            role=role,
            flf=flf,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, phone_number, role, flf, password=None, **extra_fields):
        self._create_user(
            phone_number=phone_number,
            role=role,
            flf=flf,
            password=password,
            **extra_fields,
        )
    
    def create_superuser(self, phone_number, flf, role, password=None, **extra_fields):
        user = self._create_user(
            phone_number=phone_number, password=password, role=role, flf=flf, **extra_fields
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class AdminManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=UserRoles.admin.value)


class SponsorManager(manager.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=UserRoles.sponsor.value)
    

# class StudentsManager(manager.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(role=UserRoles.student.value)

