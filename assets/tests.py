import json 

from django.urls import reverse

from rest_framework import status 
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User

class AssetTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(email='company@mail.com',password='company-password')
        self.token = Token.objects.create(user=self.user)
        self.user.is_company = True # so it is authorized to get permissions as company
        self.user.save() 
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
    
    def test_add_employee(self):
        # initially adding an employee
        # who is not registered yet
        data = {
            "employee_email":"employee@mail.com"
        }
        response = self.client.post('/api/v1/assets/add/employee/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Employee is not registered")

        # signup an employee to add
        data = {
            'name': 'employee',
            'email': 'employee@mail.com',
            'password': 'employee-password'
        }
        response = self.client.post('/api/v1/accounts/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = {
            "employee_email": "employee@mail.com"
        }

        # now trying to add employee from a not-company account
        self.user.is_company = False 
        self.user.save()
        response = self.client.post('/api/v1/assets/add/employee/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # from a company account
        self.user.is_company = True
        self.user.save()
        response = self.client.post('/api/v1/assets/add/employee/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # now trying to add an employee who is already
        # added to any company
        response = self.client.post('/api/v1/assets/add/employee/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_device(self):
        data = {
            "device_id": "001",
            "type": "Phone",
            "brand": "Sumsang",
            "model": "22S"
        }

        response = self.client.post('/api/v1/assets/add/device/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # adding with same device id
        response = self.client.post('/api/v1/assets/add/device/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # adding from not company
        data['device_id'] = 'DI_002'
        self.user.is_company = False
        self.user.save()
        response = self.client.post('/api/v1/assets/add/device/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_hand_out_return(self):
        employee_data = {
            'name': 'employee',
            'email': 'employee@mail.com',
            'password': 'employee-password'
        }

        response = self.client.post("/api/v1/accounts/signup/", data=employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "employee_email": "employee@mail.com"
        }

        response = self.client.post("/api/v1/assets/add/employee/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "device_id": "DI_001",
            "type": "Phone",
            "brand": "Sumsang",
            "model": "22S",
        }

        response = self.client.post('/api/v1/assets/add/device/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "employee_email": "employee@mail.com",
            "device_id": "DI_001",
            "condition": "Good"
        }

        response = self.client.post("/api/v1/assets/handout_device/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            "return_condition": "Good"
        }

        response = self.client.patch("/api/v1/assets/return_device/1", data=data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['return_condition'], data['return_condition'])

        response = self.client.get("/api/v1/assets/device_logs")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
