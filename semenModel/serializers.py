from rest_framework import serializers
from .models import ImageData


class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = '__all__'

    def create(self, validated_data):
        return ImageData.objects.create(**validated_data)
