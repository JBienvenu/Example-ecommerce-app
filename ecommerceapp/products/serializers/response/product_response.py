from rest_framework import serializers
from products import models


class ProductReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = serializers.ALL_FIELDS
