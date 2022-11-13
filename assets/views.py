from urllib import response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import user_passes_test

from .serializers import DeviceSerializer, CompanyEmployeeSerializer, LogSerializer
from accounts.models import User
from .models import Device, Log, CompanyEmployee

class AddDeviceView(generics.GenericAPIView):
    serializer_class = DeviceSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request: Request):
        user = request.user
        if user.is_authenticated and user.is_company:

            data = request.data
            
            data['owner'] = user.pk
            serialized = self.serializer_class(data=data)

            if serialized.is_valid():
                serialized.save()

                response = {
                    "message": "Device added",
                    "data": serialized.data
                }

                return Response(data=response, status=status.HTTP_201_CREATED)      
            return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "Unauthorized"}, status=status.HTTP_400_BAD_REQUEST)

class AddEmployeeView(generics.GenericAPIView):
    serializer_class = CompanyEmployeeSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request: Request):
        user = request.user
        if user.is_authenticated and user.is_company:

            employee_email = request.data['employee_email']
            print(employee_email)
            data = {}
            if User.objects.filter(email=employee_email).exists():
                employee = User.objects.get(email=employee_email).pk
                if not employee.is_company:
                    return Response(data={"message":"Provide an employee mail"}, status=status.HTTP_400_BAD_REQUEST)
                data['employee'] = employee
            else:
                return Response(data={"message":"Employee is not registered"}, status=status.HTTP_400_BAD_REQUEST)

            data['company'] = user.pk
            serialized = self.serializer_class(data=data)

            if serialized.is_valid():
                serialized.save()

                response = {
                    "message": "Employee added",
                    "data": serialized.data
                }

                return Response(data=response, status=status.HTTP_201_CREATED)      
            return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "Unauthorized"}, status=status.HTTP_400_BAD_REQUEST)

class HandoutDeviceView(generics.GenericAPIView):
    serializer_class = LogSerializer
    authentication_classes = [TokenAuthentication]

    def post(self, request: Request):
        user = request.user 
        
        if user.is_authenticated and user.is_company:
            employee_email = request.data['employee_email']
            device_id = request.data['device_id']
            condition = request.data['condition']
            data = {}
            # data['handed_to'] = 
            if Device.objects.filter(device_id=device_id, owner=user.pk).exists():
                device = Device.objects.filter(device_id=device_id, owner=user)[0]
                employee = User.objects.filter(email=employee_email)[0]
                print(employee)
                is_employee_company = CompanyEmployee.objects.filter(company=user.pk, employee=employee).exists()
                if device.is_available and is_employee_company:
                    data['device'] = device.pk
                    data['handed_to'] = employee.pk
                    data['checkout_condition'] = condition
                    serialized = self.serializer_class(data=data)
                    if serialized.is_valid():
                        serialized.save()

                        response = {
                            "message": "Handed out successfully",
                            "data": serialized.data
                        }

                        return Response(data=response, status=status.HTTP_201_CREATED)      
                    return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(data={"message":"Employee or Device not available"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"message": "Unauthorized"}, status=status.HTTP_400_BAD_REQUEST)