from urllib import response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.decorators import user_passes_test

from .serializers import DeviceSerializer
from accounts.models import User

class AddDeviceView(generics.GenericAPIView):
    serializer_class = DeviceSerializer
    authentication_classes = [TokenAuthentication]

    @csrf_exempt
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