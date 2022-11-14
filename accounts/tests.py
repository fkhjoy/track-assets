import json 

from django.urls import reverse

from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User

class SingupTestCase(APITestCase):

    def test_signup(self):
        data = {
            "name": "Test User",
            "email": "test@mail.com",
            "password": "testpassword"
        }
        response = self.client.post("/api/v1/accounts/signup/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/api/v1/accounts/signup/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
