from django.urls import path
from users.apps import UsersConfig
from users.views import UserUpdateAPIView, PaymentCreateAPIVew, PaymentListAPIView, PaymentRetrieveAPIView, \
    UserCreateAPIView, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('users/register/', UserCreateAPIView.as_view(), name='user_register'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_profile'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('payment/create/', PaymentCreateAPIVew.as_view(), name='payment_create'),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
]