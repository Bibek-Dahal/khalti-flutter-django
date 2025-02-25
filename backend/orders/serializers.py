
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','name','quantity','price','image_url','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

from rest_framework import serializers

class KhaltiPaymentSerializer(serializers.Serializer):
    return_url = serializers.URLField(required=True)
    website_url = serializers.URLField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    name = serializers.CharField(max_length=255, required=True)
    image_url = serializers.URLField(required=False, allow_null=True)
    user_id = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(required=True)
