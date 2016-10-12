import uuid
from datetime import datetime
from django.db import models


class Product(models.Model):
    """A base class that defines base attributes of products"""
    # product_id = models.UUIDField(
    #     primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=300, blank=False)
    display_name = models.CharField(max_length=300, blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True, default="")
    price = models.FloatField(blank=False)
    in_stock = models.BooleanField(default=True, blank=True)
    featured = models.BooleanField(default=False, blank=True)
    created_on = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    seller_name = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True
