from rest_framework import serializers
from .models import *







class FineSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Fine
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ='__all__'
