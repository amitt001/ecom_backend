
from django.db import models
from .product import Product

MEMORY_CHOICE = (
    (16, '16 GB'),
    (32, '32 GB'),
    (64, '64 GB'))

OS_CHOICE = (
    ('ANDROID', 'Android'),
    ('IOS', 'IOS'))

class Mobile(models.Model):
    """Category: MOBILE"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    colour = models.CharField(max_length=10)
    memory = models.IntegerField(choices=MEMORY_CHOICE, blank=False)
    os = models.CharField(max_length=10, choices=OS_CHOICE, blank=False)
    ram = models.SmallIntegerField(blank=False)
    processor = models.CharField(max_length=30)
    dimensions = models.CharField(max_length=30, null=True)
    weight = models.IntegerField(null=True)
    have_camera = models.NullBooleanField()
    camera_front = models.IntegerField(null=True)
    camera_back = models.IntegerField(null=True)

