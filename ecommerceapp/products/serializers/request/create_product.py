from rest_framework import serializers


class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=80, required=True, trim_whitespace=True, min_length=3
    )
    price = serializers.IntegerField(required=True, min_value=1)
