from django.urls import reverse
from django.utils.timezone import localtime
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User, SubscriptionForUpdate, Payment


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='fortest@mail.com')
        self.course = Course.objects.create(title_course='Test Course', description='Test Description', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse('users:subscription')
        data = {
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(), {"message": "Подписка добавлена"}
        )

    def test_unsubscribe(self):
        self.subscription = SubscriptionForUpdate.objects.create(user=self.user, course=self.course)
        url = reverse('users:subscription')
        data = {
            'course': self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(), {"message": "Подписка удалена"}
        )


class UserTestCase(APITestCase):

    def setUp(self):
        self.password = 'testpassword'
        self.user = User.objects.create(email='1@mail.com')
        self.user.set_password(self.password)
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        url = reverse('users:user_profile', args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('email'), self.user.email
        )

    def test_user_create(self):
        url = reverse('users:user_register')
        data = {
            'email': 'testuser@mail.ru',
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_user_list(self):
        url = reverse('users:user_list')
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "first_name": "",
                "last_name": "",
                "phone_number": None,
                "city": None,
                "avatar": None,
                "payment": []
            }
        ]
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_user_update(self):
        url = reverse('users:user_update', args=(self.user.pk,))
        data = {
            'email': self.user.email,
            'city': 'Moscow'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('city'), 'Moscow'
        )

    def test_user_login(self):
        url = reverse('users:login')
        data = {
            'email': self.user.email,
            'password': self.password
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_tokenn(self):
        login_url = reverse('users:login')
        login_data = {'email': self.user.email, 'password': self.password}
        login_response = self.client.post(login_url, login_data)
        refresh_token = login_response.data['refresh']

        refresh_url = reverse('users:token_refresh')
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)


class PaymentTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='1@mail.com')
        self.payment = Payment.objects.create(user=self.user, payment_amount=100, payment_method='Наличные')
        self.client.force_authenticate(user=self.user)

    def test_payment_retrieve(self):
        url = reverse('users:detail', args=(self.payment.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('amount'), self.payment.payment_amount
        )

    def test_payment_create(self):
        url = reverse('users:create')
        data = {
            'user': self.user.pk,
            'amount': 200,
            'method': 'Перевод'
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_payment_list(self):
        url = reverse('users:list')
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.payment.pk,
                "date": localtime(self.payment.payment_date).isoformat(),
                "amount": self.payment.payment_amount,
                "method": self.payment.payment_method,
                "user": 12,
                "course": [],
                'lesson': [],

            }
        ]
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )
