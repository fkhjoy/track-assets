from django.urls import path 
from . import views

urlpatterns = [ 
    path('add/device/', views.AddDeviceView.as_view(), name='add_device'),
    path('add/employee/', views.AddEmployeeView.as_view(), name='add_employee'),
    path('handout_device/', views.HandoutDeviceView.as_view(), name='handout_device'),
    path('device_logs', views.HandoutDeviceView.as_view(), name='device_logs'),
    path('device_log/<int:pk>', views.ReturnDeviceView.as_view(), name='device_log'),
    path('return_device/<int:pk>', views.ReturnDeviceView.as_view(), name='return_device'),

]