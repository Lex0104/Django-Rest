from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', 'city', 'avatar')


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserDetailSerializer(ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'city', 'avatar', 'payment')