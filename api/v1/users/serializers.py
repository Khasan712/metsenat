from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from api.v1.users.models import (
    ApplicationForSponsor,
    User
)



class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            'flf',
            'role',
            'physicalPerson',
            'legalEntity',
            'password',
            'password2'
        )

        extra_kwargs = {
            "password": {"write_only": True},
        }
    def save(self, **kwargs):
        user = User(
            phone_number=self.validated_data["phone_number"],
            flf=self.validated_data["flf"],
            role=self.validated_data["role"],
            physicalPerson=self.validated_data["physicalPerson"],
            legalEntity=self.validated_data["legalEntity"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match"})
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(phone_number=obj['phone_number'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = User
        fields = ['password','phone_number','tokens']
    def validate(self, attrs):
        phone_number = attrs.get('phone_number','')
        password = attrs.get('password','')
        user = auth.authenticate(phone_number=phone_number,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active or user.is_deleted:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'flf': user.flf,
            'phone_number': user.phone_number,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_admin', 'is_superuser', 'date_joined', 'last_login', 'date_updated', 'is_active', 'is_deleted', 'password')




class ApplicationForSponsorSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForSponsor
        exclude = ('created_at', 'updated_at', 'is_active', 'is_deleted')
        # fields = ('name', 'email',)
    

class ListApplicationForSponsorSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForSponsor
        exclude = ('is_deleted', 'is_active', 'updated_at')
        # fields = ('name', 'email',)
        


