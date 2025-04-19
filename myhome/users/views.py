from rest_framework.generics import UpdateAPIView

from .models import User
from .serializers import UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer