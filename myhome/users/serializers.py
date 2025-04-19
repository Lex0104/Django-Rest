from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', "city", 'avatar')