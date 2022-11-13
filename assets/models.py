from django.db import models
import datetime
from accounts.models import User

class Device(models.Model):
    device_id = models.CharField(max_length=100, blank=False, null=False)
    type = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.type + "-" +self.model

class Log(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, blank=False, null=False)
    handed_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    checkout_time = models.DateTimeField(default=datetime.date.today)
    checkout_condition = models.TextField()
    return_time = models.DateTimeField(blank=True)
    return_condition = models.TextField()

    def __str__(self):
        return self.device