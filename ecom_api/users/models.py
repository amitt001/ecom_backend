from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    address = models.CharField(max_length=30, null=False)
    pin_code = models.CharField(max_length=6, null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    country = models.CharField(max_length=30, null=False)

    class Meta:
        unique_together = ('user', 'address')


class Phone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone')
    country_code = models.CharField(max_length=5, null=False)
    mobile_no = models.CharField(max_length=10, null=False)

    class Meta:
        unique_together = ('user', 'mobile_no')