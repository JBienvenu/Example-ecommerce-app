from rest_framework import serializers


class CreateCartSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=80, min_length=3, required=True, trim_whitespace=True
    )
