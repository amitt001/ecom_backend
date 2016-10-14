from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Product
from .models import Shoes
from .models import Mobiles


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        write_only_fields = ('added_by',)
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

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product')
        product = ProductSerializer(instance.product, data=product_data)
        if product.is_valid(raise_exception=True):
            product.save()
        return super(ShoesSerializer, self).update(instance, validated_data)


class MobilesSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = Mobiles

    def create(self, validated_data):
        product_set = validated_data.pop('product')
        product_obj = Product.objects.create(**product_set)
        validated_data['product'] = product_obj
        mobile = Mobiles.objects.create(**validated_data)
        return mobile

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product')
        product = ProductSerializer(instance.product, data=product_data)
        if product.is_valid(raise_exception=True):
            product.save()
        return super(MobilesSerializer, self).update(instance, validated_data)
