from django.shortcuts import render
from datetime import date, datetime
from django.utils import timezone
from api.v1.reports import serializers
from api.v1.reports.models import SponsorCash
from api.v1.reports.serializers import AddSponsorToStudentSerializer, SponsorInvestSerializer, SponsorsListSerializer
from api.v1.users import models
from api.v1.users.models import Sponsor, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import LimitOffsetPagination
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
        # if priceType:
        #     items = items.filter(priceType=priceType)
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

# def string_to_date(date):
#     if date:
#         return datetime.strptime(date, "%Y-%m-%d").replace(
#             tzinfo=timezone.get_current_timezone()
#         )


# def get_dates(request):
#     param = request.query_params
#     start_date = string_to_date(param.get("start_date", False)) or (
#             timezone.localtime(timezone.now()) - timezone.timedelta(days=7)
#     )
#     end_date = string_to_date(param.get("end_date", False)) or timezone.localtime(timezone.now())
#     return start_date, end_date


# def get_week():
#     start_date = (timezone.localtime(timezone.now()) - timezone.timedelta(days=7))
#     end_date = (timezone.localtime(timezone.now()))
#     return start_date, end_date

# def get_twoquarters():
#     start_date = (timezone.localtime(timezone.now()) - timezone.timedelta(days=180))
#     end_date = (timezone.localtime(timezone.now()))
#     return start_date, end_date


# def analysisovertime(items, params):
#     """ 
#     default 1 month
#     time filter: |today|weekly|monthly|twoquarters|year|start_date-end_date|
#     *By branch
#     *By Staff
#     *By Client
#     *By Warehouse
#     """
#     filter_items = params.get("filter_items")
#     start_time = params.get("start_time")
#     end_time = params.get("end_time")

#     to_day = date.today()

#     if filter_items == 'today':
#         items = items.filter(created_at__day=to_day.day)
#     if filter_items == 'weekly':
#         items = items.filter(created_at__range=get_week())
#     if filter_items == 'monthly':
#         items = items.filter(created_at__month=to_day.month)
#     if filter_items == 'twoquarters':
#         items = items.filter(created_at__range=get_twoquarters())
#     if filter_items == 'year':
#         items = items.filter(created_at__year=to_day.year)
#     if start_time and end_time:
#         items = items.filter(created_at__gte=start_time, created_at__lte=end_time)
#     return items


# class AnalysisOverTime(APIView):
#     permission_classes = (permissions.IsAuthenticated, IsAdmin)
#     pagination_class = paginations.CustomPagination
#     """
#     Yillik sponsor va studentlar hisobi
#     ========================================
#     Jami to'langan summa
#     Jami so'ralgan summa
#     Jami kerak summa
#     ========================================
#     """
#     queryset = User.objects.raw('SELECT id FROM users')
#     serializer_class = ShopSerializer

#     def get(self, request):
#         params = request.query_params
#         items = self.get_queryset()
#         filtered_data = analysisovertime(items, params)
#         if filtered_data:
#             started_time_year = filtered_data.first().created_at.strftime('%Y')
#             end_time_year = filtered_data.last().created_at.strftime('%Y')
#         else:
#             return Response({"success": False, "message": "Ma'lumot topilmadi."})
#         if int(end_time_year) < int(started_time_year):
#             started_time_year = filtered_data.last().created_at.strftime('%Y')
#             end_time_year = filtered_data.first().created_at.strftime('%Y')
#         yearly_data = []
#         for year in range(int(started_time_year), int(end_time_year)+1):
#             items_year = filtered_data.filter(created_at__year=year)
#             started_time_month = items_year.first().created_at.strftime('%m')
#             end_time_month = items_year.last().created_at.strftime('%m')
#             if int(end_time_month) < int(started_time_month):
#                 started_time_month = items_year.last().created_at.strftime('%m')
#                 end_time_month = items_year.first().created_at.strftime('%m')
#             monthly_data = []
#             year_data = {
#                 "year":f"{year}",
#                 "monthly_data":monthly_data
#             }
#             yearly_data.append(year_data)
#             for month in range(int(started_time_month), int(end_time_month)+1):
#                 items_month = items_year.filter(created_at__month=month)
#                 started_time_day = items_month.first().created_at.strftime('%d')
#                 end_time_day = items_month.last().created_at.strftime('%d')
#                 month_list = (
#                     (1, "Yanvar"),
#                     (2, "Fevral"),
#                     (3, "Mart"),
#                     (4, "Aprel"),
#                     (5, "May"),
#                     (6, "Iyun"),
#                     (7, "Iyul"),
#                     (8, "Avgust"),
#                     (9, "Sentyabr"),
#                     (10, "Oktyabr"),
#                     (11, "Noyabr"),
#                     (12, "Dekabr"),
#                 )
#                 for m in month_list:
#                     if month == m[0]:
#                         that_month = m[1]
#                 daily_data = []
#                 month_data = {
#                     "month":f"{that_month}",
#                     "daily_data":daily_data
#                 }
#                 monthly_data.append(month_data)
#                 for day in range(int(started_time_day), int(end_time_day)+1):
#                     daily_items = items_month.filter(created_at__day=day)
#                     items_day_none = items_month.filter(created_at__day=day, item_shop__sum_or_dollar__isnull=True)
#                     if daily_items:
#                         total_amount = daily_items.filter(created_at__day=day).aggregate(foo=Sum('item_shop__amount'))['foo']
#                         total_selling_price_sum = daily_items.filter(created_at__day=day, item_shop__sum_or_dollar='sum').aggregate(foo=Sum(F('item_shop__amount') * F('item_shop__selling_price')))['foo']
#                         total_selling_price_dollar = daily_items.filter(created_at__day=day, item_shop__sum_or_dollar='dollar').aggregate(foo=Sum(F('item_shop__amount') * F('item_shop__selling_price')))['foo']
#                         total_selling_price_none_currency = items_day_none.filter(created_at__day=day).aggregate(foo=Sum(F('item_shop__amount') * F('item_shop__selling_price')))['foo']
#                         total_income_price_sum = 0
#                         total_income_price_dollar = 0
#                         total_income_price_none_currency = 0
#                         for daily_item in daily_items:
#                             for p in daily_item.item_shop.all():
#                                 product_receipt_items = ProductReceiptItem.objects.select_related("receipt", "product")
#                                 total_income_price_sum += product_receipt_items.filter(product_id=p.product.id, receipt__dollar_or_sum='sum').aggregate(foo=Sum(F('amount') * F('cost')))['foo']
#                                 total_income_price_dollar_items = product_receipt_items.filter(product_id=p.product.id, receipt__dollar_or_sum='dollar')
#                                 if total_income_price_dollar_items:
#                                     total_income_price_dollar += total_income_price_dollar_items.aggregate(foo=Sum(F('amount') * F('cost')))['foo']
#                                 total_income_price_none_currency_items = product_receipt_items.filter(product_id=p.product.id, receipt__dollar_or_sum__isnull=True)
#                                 if total_income_price_none_currency_items:
#                                     total_income_price_none_currency += total_income_price_none_currency_items.aggregate(foo=Sum(F('amount') * F('cost')))['foo']
#                         total_daily_data = {
#                             "date": f"{day}-{month}-{year}",
#                             "total_amount": total_amount,
#                             "total_selling_price":{
#                                 "sum": total_selling_price_sum,
#                                 "dollar": total_selling_price_dollar,
#                                 "none_currency": total_selling_price_none_currency,
#                             },
#                             "total_income_price":{
#                                 "sum": total_income_price_sum,
#                                 "dollar": total_income_price_dollar,
#                                 "none_currency": total_income_price_none_currency,
#                             },
#                             "total_discount":{
#                                 "sum":1,
#                                 "dollar":1,
#                                 "none_currency":1,
#                             },
#                             "total_gross_income":{
#                                 "sum":1,
#                                 "dollar":1,
#                                 "none_currency":1,
#                             }
#                         }
#                         daily_data.append(total_daily_data)
#         return Response({"success": True, "yearly_data":yearly_data})
    

# class SponsorList(APIView):
#     def get(self):
#         sponsors = BecomeSponsor.objects.filter(is_active=True, is_deleted=False)
        
#         paginator = LimitOffsetPagination()
#         result_page = paginator.paginate_queryset(items, request)
#         serializer = ProductListSerializers(result_page, many=True)
#         paginator_response = paginator.get_paginated_response(result_page).data
#         return Response(
#             {
#                 "count": paginator_response['count'],
#                 "next": paginator_response['next'],
#                 "previous": paginator_response['previous'],
#                 "data": serializer.data,
#             },
#             status=status.HTTP_200_OK,
        # ) 
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    