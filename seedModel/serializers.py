from rest_framework import serializers
from .models import ImageData


class ImageDataSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = ImageData
        fields = '__all__'

    def create(self, validated_data):
        return ImageData.objects.create(**validated_data)

    def get_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)
