from django.db.models import fields
from rest_framework import serializers
from .models import  LogData, LiveData




class LogDataSerializer (serializers.ModelSerializer):
    class Meta:
        model = LogData
        fields = '__all__'

class LiveDataSerializer (serializers.ModelSerializer):
    class Meta:
        model = LiveData
        fields = '__all__'

# class BoardPropertySerializer (serializers.ModelSerializer):
    # class Meta:
        # model = BoardProperty
        # fields = '__all__'
# 