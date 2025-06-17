from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, PaymentCreateAPIVew, PaymentListAPIView, PaymentRetrieveAPIView, \
    UserCreateAPIView, UserRetrieveAPIView, UserListAPIView, SubscriptionForUpdateAPIVew


app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('users/', UserListAPIView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_profile'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('payment/create/', PaymentCreateAPIVew.as_view(), name='payment_create'),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
    path('login/', TokenObtainPairView.as_view(permission_classes = (AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes = (AllowAny,)), name='token_refresh'),
    path('subscription/', SubscriptionForUpdateAPIVew.as_view(), name='subscription')
]