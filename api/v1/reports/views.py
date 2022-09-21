from datetime import date, datetime
from django.utils import timezone
from api.v1.reports.models import SponsorCash, SponsorInvets, SponsorStudent
from api.v1.reports.serializers import AddSponsorToStudentSerializer, SponsorInvestSerializer, SponsorsListSerializer
from api.v1.users import models
from api.v1.users.models import Sponsor, Student, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import LimitOffsetPagination
from django.db.models.functions import Coalesce
from django.db.models import Count, Q, Sum, Avg, DecimalField, F
from django.db import models, transaction
from api.v1.users.permissions import (
    IsAdmin,
)
# Create your views here.


def string_to_date(date):
    if date:
        return datetime.strptime(date, "%Y-%m-%d").replace(
            tzinfo=timezone.get_current_timezone()
        )


def get_dates(request):
    param = request.query_params
    start_date = string_to_date(param.get("start_date", False)) or (
            timezone.localtime(timezone.now()) - timezone.timedelta(days=7)
    )
    end_date = string_to_date(param.get("end_date", False)) or timezone.localtime(timezone.now())
    return start_date, end_date


class SponsorInvestView(APIView):
    """
    Add money to cash
    """
    def post(self, request):
        data = request.data
        serializer = SponsorInvestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'message': 'Successfully invested..',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class AddSponsorToStudent(APIView):
    def post(self, request):
        serializers = AddSponsorToStudentSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({
            'success': True,
            'message': 'Successfully invested..',
            'data': serializers.data
        }, status=status.HTTP_201_CREATED)


class SponsorsList(APIView):
    def get_filter(self, items, params):
        status = params.get('status')
        priceType = params.get('priceType')
        money = params.get('money')
        start_time = string_to_date(params.get("start_time"))
        end_time = string_to_date(params.get("end_time"))
        if status:
            items = items.filter(status=status)
        if priceType == 'UZS':
            items = items.filter(uzs_money__lte=money)
        if priceType == 'USD':
            items = items.filter(usd_money__lte=money)
        if start_time and end_time:
            items = items.filter(created_at__gte=start_time, created_at__lte=end_time)
        return items


    def get(self, request):
        params = request.query_params
        items = SponsorCash.objects.select_related('sponsor',).filter(is_active=True, is_deleted=False).order_by('-id')
        sponsors = self.get_filter(items, params)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(sponsors, request)
        serializer = SponsorsListSerializer(result_page, many=True)
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



def get_week():
    start_date = (timezone.localtime(timezone.now()) - timezone.timedelta(days=7))
    end_date = (timezone.localtime(timezone.now()))
    return start_date, end_date

def get_twoquarters():
    start_date = (timezone.localtime(timezone.now()) - timezone.timedelta(days=180))
    end_date = (timezone.localtime(timezone.now()))
    return start_date, end_date


def analysisovertime(items, params):
    """ 
    time filter: |today|weekly|monthly|twoquarters|year|start_date-end_date|
    """
    filter_items = params.get("filter_items")
    start_time = params.get("start_time")
    end_time = params.get("end_time")

    to_day = date.today()

    if filter_items == 'today':
        items = items.filter(date_joined__day=to_day.day)
    elif filter_items == 'weekly':
        items = items.filter(date_joined__range=get_week())
    elif filter_items == 'monthly':
        items = items.filter(date_joined__month=to_day.month)
    elif filter_items == 'twoquarters':
        items = items.filter(date_joined__range=get_twoquarters())
    elif filter_items == 'year':
        items = items.filter(date_joined__year=to_day.year)
    elif start_time and end_time:
        items = items.filter(date_joined__gte=start_time, date_joined__lte=end_time)
    else:
        items = items.filter(date_joined__year=to_day.year)
    return items


class AnalysisOverTime(APIView):
    # permission_classes = (permissions.IsAuthenticated, IsAdmin)
    """
    Yillik sponsor va studentlar hisobi
    ========================================
    Jami to'langan summa
    Jami so'ralgan summa
    Jami kerak summa
    ========================================
    """
    queryset = Sponsor.objects.all()

    def get(self, request):
        params = request.query_params
        items = self.queryset
        
        filtered_data = analysisovertime(items, params)
        
        if filtered_data:
            started_time_year = filtered_data.first().date_joined.strftime('%Y')
            end_time_year = filtered_data.last().date_joined.strftime('%Y')
        else:
            return Response({"success": False, "message": "Ma'lumot topilmadi."})
        
        if int(end_time_year) < int(started_time_year):
            started_time_year = filtered_data.last().date_joined.strftime('%Y')
            end_time_year = filtered_data.first().date_joined.strftime('%Y')
        yearly_data = []
        
        for year in range(int(started_time_year), int(end_time_year)+1):
            items_year = filtered_data.filter(date_joined__year=year)
            started_time_month = items_year.first().date_joined.strftime('%m')
            end_time_month = items_year.last().date_joined.strftime('%m')
            if int(end_time_month) < int(started_time_month):
                started_time_month = items_year.last().date_joined.strftime('%m')
                end_time_month = items_year.first().date_joined.strftime('%m')
            monthly_data = []
            year_data = {
                "year":f"{year}",
                "monthly_data":monthly_data
            }
            yearly_data.append(year_data)
            for month in range(int(started_time_month), int(end_time_month)+1):
                items_month = items_year.filter(date_joined__month=month)
                started_time_day = items_month.first().date_joined.strftime('%d')
                end_time_day = items_month.last().date_joined.strftime('%d')
                month_list = (
                    (1, "Yanvar"),
                    (2, "Fevral"),
                    (3, "Mart"),
                    (4, "Aprel"),
                    (5, "May"),
                    (6, "Iyun"),
                    (7, "Iyul"),
                    (8, "Avgust"),
                    (9, "Sentyabr"),
                    (10, "Oktyabr"),
                    (11, "Noyabr"),
                    (12, "Dekabr"),
                )
                for m in month_list:
                    if month == m[0]:
                        that_month = m[1]
                daily_data = []
                month_data = {
                    "month":f"{that_month}",
                    "daily_data":daily_data
                }
                monthly_data.append(month_data)
                for day in range(int(started_time_day), int(end_time_day)+1):
                    daily_items = items_month.filter(date_joined__day=day)
                    if daily_items:
                        total_sponsors = daily_items.count()
                        total_students = Student.objects.filter(created_at__year=year, created_at__month=month, created_at__day=day)
                        
                        """ Jami to'langanlar UZS da """
                        total_paid_uzs = SponsorStudent.objects.select_related('sponsor', 'student').filter(
                            created_at__year=year, created_at__month=month, created_at__day=day, priceType='UZS',
                        ).aggregate(foo=Coalesce(Sum('money'), 0.0))['foo']
                        
                        
                        """ Jami to'langanlar USD da """
                        total_paid_usd = SponsorStudent.objects.select_related('sponsor', 'student').filter(
                            created_at__year=year, created_at__month=month, created_at__day=day, priceType='USD',
                        ).aggregate(foo=Coalesce(Sum('money'), 0.0))['foo']
                        
                        
                        """ Jami so'ralganlar UZS da """
                        total_asked_uzs = SponsorInvets.objects.select_related('sponsorCash',).filter(
                            created_at__year=year, created_at__month=month, created_at__day=day, priceType='UZS',
                        ).aggregate(foo=Coalesce(Sum('money'), 0.0))['foo']
                        
                        
                        """ Jami so'ralganlar USD da """
                        total_asked_usd = SponsorInvets.objects.select_related('sponsorCash',).filter(
                            created_at__year=year, created_at__month=month, created_at__day=day, priceType='USD',
                        ).aggregate(foo=Coalesce(Sum('money'), 0.0))['foo']
                        
                        
                        """ Jami to'lanishi kerak bo'lgan summa UZS da """
                        students_total_contracts = total_students.aggregate(foo=Coalesce(Sum('studentContract'), 0.0))['foo']
                        total_have_to_pay_uzs = students_total_contracts - total_paid_uzs
                        
                        # """ Jami to'lanishi kerak bo'lgan summa USD da """
                        # total_have_to_pay_usd = SponsorInvets.objects.select_related('sponsorCash',).filter(
                        #     created_at__year=year, created_at__month=month, created_at__day=day, priceType='USD',
                        # ).aggregate(foo=Coalesce(Sum('money'), 0.0))['foo']
                        
                    total_daily_data = {
                        "date": f"{day}-{month}-{year}",
                        "total_sponsors": total_sponsors,
                        "total_students": total_students.count(),
                        
                        "total_paid_uzs": total_paid_uzs,
                        "total_paid_usd": total_paid_usd,
                        
                        "total_asked_uzs": total_asked_uzs,
                        "total_asked_usd": total_asked_usd,
                        
                        "total_have_to_pay_uzs": total_have_to_pay_uzs,
                        # "total_have_to_pay_usd": total_have_to_pay_usd,
                        
                    }
                    daily_data.append(total_daily_data)
        return Response(
            {
                "success": True,
                "yearly_data":yearly_data
            }
        )


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    