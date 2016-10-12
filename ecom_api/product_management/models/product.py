import uuid
from datetime import datetime
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# (Stored, Readable value)
CATEGORY_CHOICES = (
    ('SHOE', 'Shoes'),
    ('MOBILE', 'Mobile'))


class Product(models.Model):
    """A base class that defines base attributes of products"""
    # product_id = models.UUIDField(
    #     primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    # id = models.AutoField(
    #     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
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
    seller_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ('name',)


# Product `pre_save` signal
@receiver(pre_save, sender=Product)
def pre_save_tasks(sender, instance, *args, **kwargs):
    instance.display_name = instance.name
    instance.quantity_available = instance.quantity
    instance.units_on_order = instance.quantity - instance.quantity_available
    if instance.quantity_available > 1:
        instance.in_stock = True