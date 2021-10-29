from rest_framework import serializers
from products.models import Product


class AddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Product of id {value} does not exist.", code=404)
        return value
