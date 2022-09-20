from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from api.v1.users import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('register/', views.UserRegistrationView.as_view()),
    path('login/',views.LoginAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),
    path('detail/<int:pk>/', views.DetailUserViews.as_view()),
    
    path('form/create/', views.CreateApplicationForSponsor.as_view()),
    path('form/list/', views.ListApplicationForSponsor.as_view()),
    path('form/detail/<int:pk>/', views.DetailApplicationForSponsor.as_view()),
]
