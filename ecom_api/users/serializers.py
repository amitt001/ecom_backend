from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Address, Phone


EMAIL_MOD_FAIL_MSG = dict(email=["Email can't be modified, once set"])
PSWD_REQUIRED = dict(password=["Password field is required field"])


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('address', 'city', 'state', 'pin_code', 'country')


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('country_code', 'mobile_no')


class UserSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=True)
    phone = PhoneSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name',
            'email', 'password',
            'address', 'phone')

    def ato_representation(self, obj):
        _fields = ('id', 'first_name', 'last_name', 'email')
        return dict((i, getattr(obj, i)) for i in _fields)

    def create(self, validated_data):
        print(validated_data)
        address_set = validated_data.pop('address')
        phone_set = validated_data.pop('phone')
        password = validated_data.pop('password')
        validated_data['username'] = validated_data['email']
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # address_set['user'] = user
        # phone_set['user'] = user
        for addr in address_set:
            Address.objects.create(user_id=user.id, **addr)
        for ph in phone_set:
            Phone.objects.create(user_id=user.id, **ph)
        return user

    def update(self, instance, validated_data):
        # TODO: Check all fields or call super update
        if 'email' in validated_data:
            raise serializers.ValidationError(EMAIL_MOD_FAIL_MSG)
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance
