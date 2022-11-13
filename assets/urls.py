from django.urls import path 
from . import views

urlpatterns = [ 
    path('v1/add/device/', views.AddDeviceView.as_view(), name='add_device'),

]