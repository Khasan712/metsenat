from django.urls import path

from . import views


urlpatterns = [
    path('invest/', views.SponsorInvestView.as_view()),
    path('add/sponsor-student/', views.AddSponsorToStudent.as_view()),
    path('sponsors/list/', views.SponsorsList.as_view()),
]
