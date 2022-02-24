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

# Create your views here.
class LogDataViewSet (viewsets.ModelViewSet):
    serializer_class = LogDataSerializer
    queryset = LogData.objects.all()

class LiveDataViewSet (viewsets.ModelViewSet):
    serializer_class = LiveDataSerializer
    queryset = LiveData.objects.all()


def checkDiff(currData, prevData, prev_time, present_time):
    diffdata = currData - prevData
    if diffdata < 0 :
        diffdata += cupSize
# ###############################################################################################################################################################
#  important :
#       the invalid data is going to bhe replaced with a negetive large number but not inf, sql couldn't store it
#       and the sum could be positive and cause bug
# ###############################################################################################################################################################

    # print(present_time - prev_time)
    if (present_time - prev_time) >  timeCheck:
        diffdata = -inf

    # print(diffdata)
    return diffdata

@api_view(['POST'])
def add_data(request):

    if request.method == 'POST':
        if(len(request.data)==0):
            return Response({"no data recieved"},status=status.HTTP_400_BAD_REQUEST)
        for i in range(0,len(request.data)):
            data = {}
            data['mac_addr'] = request.data[i]['mac_addr']
            data['sendDataTime'] = request.data[i]['unixTime']
            for pin in request.data[i]['Data']:
                data['pin'] = pin['pin']
                data['sensor_data'] = pin['sensor_data']
                if data['sensor_data'] == "None" :
                    continue

                diff = 0
                try:
                    livedata = LiveData.objects.get(mac_addr=data['mac_addr'], pin=data['pin'])
                    prev_data = livedata.sensor_data


                    prev_time_updated = (livedata.sendDataTime)
                    prev_time_updated = prev_time_updated.replace(tzinfo=None)
                    # print(prev_time_updated, type(prev_time_updated))
                    present_time = datetime.datetime.fromtimestamp(data['sendDataTime'])

                    diff = checkDiff(float(data['sensor_data']),float(prev_data), prev_time_updated, present_time)
                    data['diff_data'] = diff
                    data['updated_at'] = datetime.datetime.now()
                    # print("time", datetime.datetime.now())
                    # print("data",data)
                    # print("livedata model", livedata)
                    # print("unix time",data['sendDataTime'], "exchanged time", datetime.datetime.fromtimestamp(data['sendDataTime']))
                    try:
                        LiveData.objects.filter(mac_addr=data['mac_addr'], pin=data['pin']).update(sensor_data=data['sensor_data'], diff_data=data['diff_data'], updated_at=data['updated_at'].replace(tzinfo=None), sendDataTime=datetime.datetime.fromtimestamp(data['sendDataTime']).replace(tzinfo=None))
                    except:
                        return Response(traceback.print_exc(),status=status.HTTP_400_BAD_REQUEST)
                    # live_serializer = LiveDataSerializer(data=data)
                    # print("new model", live_serializer)
                    # if live_serializer.is_valid():
                        # live_serializer.save()
                        # livedata.update(live_serializer)
                    # else:
                    #     return Response(live_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except LiveData.DoesNotExist:
                    live_serializer = LiveDataSerializer(data=data)
                    if live_serializer.is_valid():
                        live_serializer.save()
                    else:
                        return Response(live_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                log_serializer = LogDataSerializer(data=data)
                if log_serializer.is_valid():
                    log_serializer.save()
                else:
                    return Response(log_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data created"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def logsInPeriod(request):
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
                        #print(LogData.objects.values('mac_addr','pin'))

                        logs_in_period = (LogData.objects
                                        .values('mac_addr','pin','sendDataTime')
                                        .filter(sendDataTime__range = (time, temp_time))
                                        .annotate(sum_of_diff = Sum('diff_data'))
                                        )

                        time = temp_time
                        if len(logs_in_period) > 0 :
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
