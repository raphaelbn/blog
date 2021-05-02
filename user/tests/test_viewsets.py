from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.tests.factories import UserFactory
from user.tests.mock import mock_authenticate_credentials_success
from user.models import User
from user.serializers import ListUserSerializer


class CreateUserViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("user:user-detail")
        self.data = {
            'displayName': 'Brett Wiltshire',
            'email': 'brett@email.com',
            'password': 123456,
            'image': 'http://4.bp.blogspot.com/_YA50adQ-7vQ/S1gfR_6ufpI/AAAAAAAAAAk/1ErJGgRWZDg/S45/brett.png'
        }

    def test_signup_success(self):
        response = self.client.post(self.url, data=self.data)

        user = User.objects.get(email='brett@email.com')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(len(response.data.get('token')), 0)
        self.assertEqual(user.displayName, 'Brett Wiltshire')

    def test_signup_missing_password(self):
        del self.data['password']
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_password_blank(self):
        self.data['password'] = ''
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_missing_display_name(self):
        del self.data['displayName']
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_displayname_blank(self):
        self.data['displayName'] = ''
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_missing_email(self):
        del self.data['email']
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_email_blank(self):
        self.data['email'] = ''
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogInViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.url = reverse("user:login")
        self.data = {
            'email': 'raphael@email.com',
            'password': '123456'
        }

    def test_login_success(self):
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.data['token']), 0)

    def test_login_wrong_password(self):
        self.data['password'] = 'wrong_password'

        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'Campos inválidos')

    def test_login_missing_password(self):
        del self.data['password']

        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"password\" is required')

    def test_login_empty_password(self):
        self.data['password'] = ''

        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"password\" is not allowed to be empty')

    def test_login_wrong_email(self):
        self.data['email'] = 'wrong@email.com'

        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('message'), 'Campos inválidos')

    def test_login_missing_email(self):
        del self.data['email']

        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"email\" is required')

    def test_login_empty_email(self):
        self.data['email'] = ''

        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"email\" is not allowed to be empty')


class GetUserViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.url = reverse('user:get', kwargs={'pk': self.user[0].id})

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_get_user_success(self):
        response = self.client.get(self.url)

        user_serializer = ListUserSerializer(self.user[0])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, user_serializer.data)

    def test_get_user_missing_token_authorization(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_get_user_404(self):
        response = self.client.get(f'{self.url[:6]}99999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ListUsersViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.user2 = UserFactory.create_batch(size=1, displayName='raphael bezerra', email='raphael2@email.com', password='123457')
        self.url = reverse('user:user-detail')

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_get_list_user_success(self):
        response = self.client.get(self.url)

        user_serializer = ListUserSerializer([self.user[0], self.user2[0]], many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, user_serializer.data)

    def test_get_list_user_missing_token_authorization(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteUserViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, displayName='Brett Wiltshire', email='brett@email.com', password='123456')
        self.url = reverse('user:delete')

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_delete_user_success(self):
        response = self.client.delete(self.url)

        user = User.objects.filter(email='brett@email.com')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {})
        self.assertFalse(user.exists())

    def test_delete_user_missing_token_authorization(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
