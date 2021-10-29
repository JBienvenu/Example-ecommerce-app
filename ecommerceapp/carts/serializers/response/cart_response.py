from rest_framework import serializers
from carts import models


class CartResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = serializers.ALL_FIELDS
