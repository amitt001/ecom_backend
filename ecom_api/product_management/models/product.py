import uuid
from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.exceptions import FieldError
from django.dispatch import receiver

from django.contrib.auth.models import User

# (Stored, Readable value)
CATEGORY_CHOICES = (
    ('Shoes', 'Shoes'),
    ('Mobiles', 'Mobiles'))


class Product(models.Model):
    """A base class that defines base attributes of products"""
    # TODO: maybe add uniqueness to some fields
    # TODO: in category add multiple size support
    name = models.CharField(max_length=300, blank=False)
    display_name = models.CharField(max_length=300, blank=True)
    category = models.CharField(
        max_length=30, choices=CATEGORY_CHOICES, blank=False)
    manufacturer = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True, default="")
    # Price details
    price = models.FloatField(blank=False)
    discount_amount = models.FloatField(default=0.0)
    # Order specific details
    quantity = models.IntegerField(blank=False, default=0)
    quantity_available = models.IntegerField(blank=True, default=0)
    units_on_order = models.IntegerField(blank=True, default=0)
    in_stock = models.BooleanField(default=True, blank=True)
    featured = models.BooleanField(default=False, blank=True)
    created_on = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    # Id of the user added this product
    seller = models.IntegerField(null=False, default=0)
    added_by = models.IntegerField(null=False, default=0)

    class Meta:
        ordering = ('name',)

@receiver(pre_save, sender=Product)
def pre_save_task(sender, instance, *args, **kwargs):
    if instance.quantity_available > instance.quantity:
        raise FieldError('quantity_available can\'t be more than quantity')
    if instance.units_on_order > instance.quantity_available:
        raise FieldError('units_on_order can\'t be more than quantity')

# Product `pre_save` signal
@receiver(post_save, sender=Product)
def post_save_tasks(sender, instance, *args, **kwargs):
    if not instance.display_name:
        instance.display_name = instance.name
    if not instance.quantity_available:
        instance.quantity_available = instance.quantity
        instance.units_on_order = instance.quantity - instance.quantity_available
    if instance.quantity_available > 1:
        instance.in_stock = True
