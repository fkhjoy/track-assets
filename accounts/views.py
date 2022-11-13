from urllib import response
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import SignUpSerializer

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        data = request.data 

        serialized = self.serializer_class(data=data)

        if serialized.is_valid():
            serialized.save()

            response = {
                "message": "User created",
                "data": serialized.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serialized.errors, status=status.HTTP_400_BAD_REQUEST)