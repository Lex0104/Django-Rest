from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import User, Payment, SubscriptionForUpdate
from users.serializers import UserSerializer, PaymentSerializer, UserRegisterSerializer, UserDetailSerializer, \
    UserDetailPublicSerializer
from users.services import create_stripe_price, create_stripe_product, create_stripe_session


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        user_id = self.kwargs['pk']
        if user_id == self.request.user.id:
            return UserDetailSerializer
        return UserDetailPublicSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class PaymentCreateAPIVew(CreateAPIView):
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(id=course_id)
        course_title = course.title_course
        course_price = course.price
        payment = serializer.save(user=self.request.user, payment_amount=course_price)
        payment.payment_course.add(course)
        stripe_product_id = create_stripe_product(course_title)
        stripe_price = create_stripe_price(course_price, stripe_product_id)
        session_id, payment_url = create_stripe_session(stripe_price)
        payment.session_id = session_id
        payment.url = payment_url
        payment.save()


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ['date']


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class SubscriptionForUpdateAPIVew(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = SubscriptionForUpdate.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            SubscriptionForUpdate.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
        return Response({"message": message})