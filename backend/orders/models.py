from django.db import models
from django.contrib.auth.models import User
import uuid
class OrderStatus(models.TextChoices):
    STARTED = 'started', 'Started'
    INITIATED = 'initiated', 'Initiated'
    COMPLETED = 'completed', 'Completed'
    CANCELED = 'canceled', 'Canceled'
    USER_CANCELED = 'user_canceled', 'User Canceled'
    EXPIRED = 'expired', 'Expired'
    REFUNDED = 'refunded', 'Refunded'
    PARTIALLY_REFUNDED = 'partially_refunded', 'Partially Refunded'

# Create your models here.
class Order(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default= uuid.uuid4,
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    name = models.CharField(max_length=200)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image_url = models.URLField(null=True,blank=True)
    order_status = models.CharField(max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.STARTED)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True)