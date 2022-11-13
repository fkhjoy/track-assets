from django.contrib import admin
from .models import Device, Log, CompanyEmployee

admin.site.register(Device)
admin.site.register(Log)
admin.site.register(CompanyEmployee)
