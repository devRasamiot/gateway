from django.db.models.fields import DateTimeField
from django.shortcuts import render
from rest_framework import serializers, viewsets
from .serializers import LogDataSerializer, LiveDataSerializer
from .models import LogData, LiveData
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
import requests
from django.http import HttpResponse, JsonResponse, response
from django.forms.models import model_to_dict
from django.db.models import Avg, Count, Sum, F, DateTimeField
import datetime
from django.utils.dateparse import parse_datetime
from .configData import cupSize, inf, timeCheck
import traceback


@api_view(['POST'])
def logsInPeriodAggre(request):
    if request.method == 'POST':        
        if ('start_time' in request.data) and ('end_time' in request.data) and ('dur_time' in request.data):
            if (request.data['start_time'] and request.data['end_time'] and request.data['dur_time']):
                response =[]
                time = parse_datetime(request.data['start_time'])
                time2 = parse_datetime(request.data['end_time'])
                try:
                    # logs_in_shift = (LogData.objects
                    #                     .values('mac_addr','pin', 'sendDataTime')
                    #                     .annotate(sum_of_diff = Sum('diff_data'))
                    #                     )
                    # response.append((logs_in_shift))   
                    
                    ####
                    
                    while time < time2:
                        temp_time = time + datetime.timedelta(minutes=float(request.data['dur_time']))
                        
                        logs_in_period = (LogData.objects
                                        .values('mac_addr','pin')
                                        .filter(sendDataTime__range = (time, temp_time))
                                        .annotate(sum_of_diff = Sum('diff_data'))
                                        )
                        time = temp_time
                        response.append((logs_in_period))   
                        # if logs_in_shift : 
                        #     response.append((logs_in_shift))                
                    ####

                    # logs_in_shift = (LogData.objects.filter(sendDataTime__range = (time, time2))
                    #                     .extra(select={'sendDataTime_slice': "FLOOR (EXTRACT (EPOCH FROM sendDataTime) / '900' )"})
                    #                     .values('mac_addr','pin', 'sendDataTime_slice')
                    #                     .annotate(sum_of_diff = Sum('diff_data'))
                    #                     )
                    # response.append((logs_in_shift))   

                    ####

                    return Response((response), status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                    return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"},status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def logsInPeriodData(request):
    if request.method == 'POST':        
        if ('start_time' in request.data) and ('end_time' in request.data) :
            if (request.data['start_time'] and request.data['end_time']) :
                response =[]
                time = parse_datetime(request.data['start_time'])
                time2 = parse_datetime(request.data['end_time'])
                try:
                    logs_in_period = (LogData.objects
                                        .values('mac_addr','pin', 'sensor_data', 'sendDataTime')
                                        .filter(sendDataTime__range = (time, time2))
                                        )
                    response.append((logs_in_period))   
                    return Response((logs_in_period), status=status.HTTP_200_OK)
                except:
                    traceback.print_exc()
                    return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"no time specified"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"no time specified"},status=status.HTTP_400_BAD_REQUEST)
