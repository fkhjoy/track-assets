from django.urls import path 
from rest_framework.authtoken.views import obtain_auth_token

from . import views 

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', obtain_auth_token),
]