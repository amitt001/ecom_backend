from rest_framework import serializers
from .models import Product
from .models import Shoes
from .models import Mobile


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('id',)

class ShoesSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = Shoes

    def create(self, validated_data):
        product_set = validated_data.pop('product')
        product_obj = Product.objects.create(**product_set)
        validated_data['product'] = product_obj
        shoe = Shoes.objects.create(**validated_data)
        return shoe


class MobileSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = Mobile

    def create(self, validated_data):
        product_set = validated_data.pop('product')
        product_obj = Product.objects.create(**product_set)
        validated_data['product'] = product_obj
        mobile = Mobile.objects.create(**validated_data)
        return mobile

