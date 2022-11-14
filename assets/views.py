from collections import OrderedDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from .serializers import DeviceSerializer, CompanyEmployeeSerializer, LogSerializer
from accounts.models import User
from .models import Device, Log, CompanyEmployee

class AddDeviceView(generics.GenericAPIView):
    serializer_class = DeviceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        user = request.user
        # checking if the user is company or not
        if user.is_company:
            data = {}
            data["device_id"] = request.data["device_id"]
            data["type"] = request.data["type"]
            data["brand"] = request.data["brand"]
            data["model"] =  request.data["model"]
            
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
        return Response(data={"message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

class AddEmployeeView(generics.GenericAPIView):
    serializer_class = CompanyEmployeeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request):
        user = request.user
        #checking if the user is company or not
        if user.is_company:

            employee_email = request.data['employee_email']
            data = {}

            # checking if the email is registered and employee or not
            if User.objects.filter(email=employee_email).exists():
                employee = User.objects.get(email=employee_email)
                if employee.is_company:
                    return Response(data={"message":"Provide an employee mail"}, status=status.HTTP_400_BAD_REQUEST)
                data['employee'] = employee.pk
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
        return Response(data={"message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)

class HandoutDeviceView(generics.GenericAPIView):
    serializer_class = LogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        user = request.user

        if user.is_company:
            devices = Log.objects.filter(device__owner=user.pk).all()
            serialized = self.serializer_class(devices, many=True)
            return Response(serialized.data)
        return Response(data={"message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    def post(self, request: Request):
        user = request.user 
        
        # checking if the user is company or not
        if user.is_company:
            employee_email = request.data['employee_email']
            device_id = request.data['device_id']
            condition = request.data['condition']
            data = {}
            # checking if the device is under the company
            if Device.objects.filter(device_id=device_id, owner=user.pk).exists():
                device = Device.objects.filter(device_id=device_id, owner=user)[0]
                employee = User.objects.filter(email=employee_email)[0]
                
                # checking if the employee is under the company
                is_employee_company = CompanyEmployee.objects.filter(company=user.pk, employee=employee).exists()
                
                # hand out if the device is available and employee under the company
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
                        # updating the device availability to False, so others can't take this
                        device.is_available = False
                        device.save()

                        return Response(data=response, status=status.HTTP_201_CREATED)      
                    return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(data={"message":"Employee or Device not available"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"message":"Device not available"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)


class ReturnDeviceView(generics.GenericAPIView):
    serializer_class = LogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user_id):
        try:
            return Log.objects.get(pk=pk, device__owner=user_id)
        except Log.DoesNotExist:
            raise Http404

    def patch(self, request:Request, pk):
        user = request.user
        # checking if the user is company
        if user.is_company:
            # getting the log for the device along company constraint
            log = self.get_object(pk, user.pk)
            log.return_time = timezone.now() # updating the return time
            serialized = self.serializer_class(log, data=request.data, partial=True)
            if serialized.is_valid():
                device = log.device
                device.is_available = True 
                device.save()
                serialized.save()
                return Response(serialized.data)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message":"Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request: Request, pk):
        user = request.user
        if user.is_company:
            log = self.get_object(pk, user.pk)
            serialized = self.serializer_class(log)
            return Response(serialized.data)
        return Response(data={"message":"Not authorized"}, status=status.HTTP_401_UNAUTHORIZED)