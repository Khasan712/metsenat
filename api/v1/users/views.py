from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import LimitOffsetPagination

from api.v1.users.models import (
    ApplicationForSponsor,
    Sponsor,
    Student,
    User,
)
from api.v1.users.serializers import (
    DetailStudentSerializers,
    LoginSerializer,
    LogoutSerializer,
    RegisterUserSerializer,
    ApplicationForSponsorSerializers,
    ListApplicationForSponsorSerializers,
    StudentSerializers,
    StudentSponsorsSerializers,
    UserUpdateSerializer,
    RegisterSponsorSerializer
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
        
class SponsorRegistrationView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    serializer_class = RegisterSponsorSerializer
    queryset = Sponsor.objects.all()

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



class StudentCreate(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializers

class ListStudent(APIView):
    
    def get_filter(self, items, request):
        params = request.query_params
        studentType = params.get("studentType")
        iohe = params.get("iohe")
        if studentType:
            items = items.filter(studentType=studentType)
        if iohe:
            items = items.filter(iohe=iohe)
        return items
    
    def get(self, request):
        items = Student.objects.filter(is_active=True, is_deleted=False)
        students = self.get_filter(items, request)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(students, request)
        serializer = DetailStudentSerializers(result_page, many=True)
        paginator_response = paginator.get_paginated_response(result_page).data
        return Response(
            {
                "count": paginator_response['count'],
                "next": paginator_response['next'],
                "previous": paginator_response['previous'],
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.filter(is_active=True, is_deleted=False)
    serializer_class = StudentSerializers


class StudentSponsorsView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSponsorsSerializers
        



class CreateApplicationForSponsor(generics.CreateAPIView):
    queryset = ApplicationForSponsor.objects.all()
    serializer_class = ApplicationForSponsorSerializers
    

class ListApplicationForSponsor(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    queryset = ApplicationForSponsor.objects.filter(is_active=True, is_deleted=False)
    # queryset = ApplicationForSponsor.objects.raw('SELECT id, is_active, is_deleted FROM users_applicationforsponsor WHERE is_active=true AND is_deleted=false')
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