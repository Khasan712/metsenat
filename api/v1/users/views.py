from functools import partial
from django.shortcuts import render
from api.v1.users import serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from api.v1.users.models import (
    ApplicationForSponsor,
    User,
)
from api.v1.users.serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterUserSerializer,
    ApplicationForSponsorSerializers,
    ListApplicationForSponsorSerializers,
    UserUpdateSerializer
)
from api.v1.users.permissions import (
    IsAdmin,
)

# Create your views here.


class UserRegistrationView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()

    def post(self, request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(
            {
                "success": True,
                "message": 'User created suucessfully.',
                "error": [],
                "data": user_data,
            }, status=status.HTTP_201_CREATED
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        return Response(
            {
                "success": True,
                "message": 'User logged suucessfully.',
                "error": [],
                "data": user_data,
            }, status=status.HTTP_200_OK
        )
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "message": 'User logged out suucessfully.',
                "error": [],
                "data": {},
            }, status=status.HTTP_204_NO_CONTENT
        )


class DetailUserViews(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    
    # def get_object(self, pk):
    #     try:
    #         item = User.objects.get(id=pk)
    #     except User.DoesNotExist:
    #         return None
    #     return item
    
    # def get(self, request, pk):
    #     item = self.get_object(pk)
    #     if item:
    #         serializer = UserUpdateSerializer(item)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response({
    #         'success': False,
    #         'message': 'User not found !'
    #     })
    
    # def patch(self, request, pk):
    #     item = self.get_object(pk)
    #     if item:
    #         serializer = UserUpdateSerializer(item, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response({
    #         'success': False,
    #         'message': 'User not found !'
    #     })


class CreateApplicationForSponsor(generics.CreateAPIView):
    queryset = ApplicationForSponsor.objects.all()
    serializer_class = ApplicationForSponsorSerializers
    

class ListApplicationForSponsor(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    queryset = ApplicationForSponsor.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ListApplicationForSponsorSerializers


class DetailApplicationForSponsor(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        queryset = ApplicationForSponsor.objects.filter(is_active=True, is_deleted=False)
        return queryset
    
    
    
    def get_object(self, pk):
        try:
            item = self.get_queryset().get(pk=pk)
        except:
            return None
        return item
    
    
    def get(self, request, pk):
        item = self.get_object(pk)
        if item:
            return Response({
                'success': True,
                'message': 'Successfully.',
                'data': ListApplicationForSponsorSerializers(item).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'User not found !',
            }, status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self, request, pk):
        item = self.get_object(pk)
        if item:
            serializer = ListApplicationForSponsorSerializers(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Successfully.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'User not found !',
            }, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        try:
            item = self.get_object(pk)
            item.is_active = False
            item.is_deleted = True
            item.save()
        except Exception as e:
            return Response({
                'success': False,
                'message': 'User not found !',
                # 'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'success': True,
                'message': 'Successfully deleted.',
            }, status=status.HTTP_200_OK)