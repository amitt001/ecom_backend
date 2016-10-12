"""Product category: Shoes

Inherits from `models.Product` and adds new attributes specific
to this category"""

from .product import Product

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


SHOE_TYPE_CHOICES = (
    ('Sports', 'SPORTS'),
    ('Running', 'RUNNING'),
    ('Casual', 'CASUAL'),
    ('Formal', 'FORMAL'),
    ('Mountaineering', 'MOUNTAINEERING')
    )


class Shoes(Product):
    size = models.FloatField(blank=False)
    colour = models.CharField(max_length=10)
    shoe_type = models.CharField(max_length=20, choices=SHOE_TYPE_CHOICES, default='CASUAL')

# Product `pre_save` signal
@receiver(pre_save)
def pre_save_tasks(sender, instance, *args, **kwargs):
    if sender in [Shoes]:
        instance.display_name = instance.name