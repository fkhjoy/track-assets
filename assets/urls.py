from django.urls import path 
from . import views

urlpatterns = [ 
    path('v1/add/device/', views.AddDeviceView.as_view(), name='add_device'),
    path('v1/add/employee/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('v1/handout_device/', views.HandoutDeviceView.as_view(), name='handout_device'),

]