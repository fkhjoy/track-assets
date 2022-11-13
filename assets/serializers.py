from rest_framework import serializers
from .models import Device, Log, CompanyEmployee

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log 
        fields = '__all__'

class CompanyEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyEmployee
        fields = '__all__'