from .models import UserData
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'email', 'name', 'surname', 'password']

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name'],
                                       surname=validated_data['surname']
                                       )
        user.set_password(validated_data['password'])
        user.save()
        return user
