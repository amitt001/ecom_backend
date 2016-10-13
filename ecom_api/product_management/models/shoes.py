"""Product category: Shoes

Inherits from `models.Product` and adds new attributes specific
to this category"""

from .product import Product
from django.db import models


SHOE_TYPE_CHOICES = (
    ('SPORT', 'Sports'),
    ('RUNNING', 'Running'),
    ('CASUAL', 'Casuals'),
    ('FORMAL', 'Formals'),
    ('MOUNTAINEERING', 'Mountaineering'))


class Shoes(models.Model):
    """Category: SHOE"""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    size = models.FloatField(blank=False)
    colour = models.CharField(max_length=10)
    shoe_type = models.CharField(
        max_length=20, choices=SHOE_TYPE_CHOICES, default='RUNNING')
