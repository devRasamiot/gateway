from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL


# Create your models here.

# class BoardProperty(models.Model):
    # mac_addr = models.CharField(max_length=100, unique=True)
    # node_id = models.CharField(max_length=100, unique=True)
# 
    # def __str__(self):
        # return self.mac_addr

class LogData(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    sendDataTime = models.DateTimeField(auto_now_add=True) 
    sensor_data = models.CharField(max_length=200)
    diff_data = models.FloatField(default=0)
    # board = models.ForeignKey(BoardProperty, on_delete=CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'{self.mac_addr}, {self.sensor_data}, {self.diff_data}'




class LiveData(models.Model):
    mac_addr = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    sendDataTime = models.DateTimeField(auto_now_add=True) 
    sensor_data = models.CharField(max_length=200)
    diff_data = models.FloatField(default=0)
    # counter = models.IntegerField()
    # board = models.ForeignKey(BoardProperty, on_delete=CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'{self.mac_addr}, {self.sensor_data}, {self.diff_data}'


