from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from post.models import Post
from post.serializers import EditPostBlogSerializer, PostBlogSerializer, ListPostSerializer
from post.tests.factories import PostFactory
from user.tests.mock import mock_authenticate_credentials_success
from user.tests.factories import UserFactory


class CreatePostViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("post:post-list")
        self.user = UserFactory.create_batch(size=1, id=401465483996, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.data = {
            'title': 'Latest updates, August 1st',
            'content': 'The whole text for the blog post goes here in this key'
        }

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_create_post_success(self):
        response = self.client.post(self.url, data=self.data)

        post = Post.objects.get(title='Latest updates, August 1st')
        post_serializer = PostBlogSerializer(post)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_serializer.data, response.data)

    def test_create_post_missing_auth(self):
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_create_post_missing_title(self):
        del self.data['title']
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"title\" is required')

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_create_post_missing_content(self):
        del self.data['content']
        response = self.client.post(self.url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"content\" is required')


class ListPostViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("post:post-list")
        self.user = UserFactory.create_batch(size=1, id=401465483996, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.post = PostFactory.create_batch(size=2, title='title of the post', content='Content of the post', user_id=self.user[0].id)

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_list_post_success(self):
        response = self.client.get(self.url)

        post_serializer = ListPostSerializer(self.post, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_serializer.data, response.data)

    def test_list_post_missing_auth(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetPostViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, id=401465483996, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.post = PostFactory.create_batch(size=1, title='title of the post', content='Content of the post', user_id=self.user[0].id)
        self.url = reverse("post:post-detail", kwargs={'pk': self.post[0].id})

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_get_post_success(self):
        response = self.client.get(self.url)

        post_serializer = ListPostSerializer(self.post[0])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_serializer.data, response.data)

    def test_get_post_missing_auth(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PutPostViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, id=401465483996, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.post = PostFactory.create_batch(size=1, title='title of the post', content='Content of the post', user_id=self.user[0].id)

        self.user2 = UserFactory.create_batch(size=1, id=54684, displayName='Brett Wiltshire', email='brett@email.com', password='654321')
        self.post2 = PostFactory.create_batch(size=1, title='title of the post', content='Content of the post', user_id=self.user2[0].id)
        self.url = reverse("post:post-detail", kwargs={'pk': self.post[0].id})
        self.data = {
            'title': 'Title edited',
            'content': 'Content edited'
        }

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_put_post_success(self):
        response = self.client.put(self.url, self.data)

        post_filtered = Post.objects.get(id=self.post[0].id)
        post_edited_serializer = EditPostBlogSerializer(post_filtered)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, post_edited_serializer.data)

    def test_put_post_missing_auth(self):
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_put_post_missing_title(self):
        del self.data['title']
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"title\" is required')

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_put_post_missing_content(self):
        del self.data['content']
        response = self.client.put(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0].get('message'), '\"content\" is required')

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_put_post_other_user(self):
        response = self.client.put(f'{self.url[:6]}{self.post2[0].id}', self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('message'), 'Usuário não autorizado')


class DeletePostViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, id=401465483996, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.post = PostFactory.create_batch(size=1, title='title of the post', content='Content of the post', user_id=self.user[0].id)

        self.user2 = UserFactory.create_batch(size=1, id=54684, displayName='Brett Wiltshire', email='brett@email.com', password='654321')
        self.post2 = PostFactory.create_batch(size=1, title='title of the post', content='Content of the post', user_id=self.user2[0].id)
        self.url = reverse("post:post-detail", kwargs={'pk': self.post[0].id})

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_delete_post_success(self):
        response = self.client.delete(self.url)

        posts = Post.objects.all()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {})
        self.assertEqual(len(posts), 1)

    def test_delete_post_missing_auth(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_delete_post_404(self):
        response = self.client.delete(f'{self.url[:6]}99999')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get('message'), 'Post não existe')

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_delete_post_other_user(self):
        response = self.client.delete(f'{self.url[:6]}{self.post2[0].id}')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get('message'), 'Usuário não autorizado')


class SearchPostViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory.create_batch(size=1, id=401465483996, displayName='raphael nascimento', email='raphael@email.com', password='123456')
        self.post = PostFactory.create_batch(size=1, title='title of the post', content='Content of the post', user_id=self.user[0].id)
        self.post2 = PostFactory.create_batch(size=1, title='title of the second post', content='Content of the second post', user_id=self.user[0].id)
        self.url = reverse("post:search")

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_search_post_by_title_success(self):
        response = self.client.get(f'{self.url}?q=title of the post')

        post_serializer = ListPostSerializer(self.post, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_serializer.data, response.data)

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_search_post_by_content_success(self):
        response = self.client.get(f'{self.url}?q=Content of the second')

        post_serializer = ListPostSerializer(self.post2, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_serializer.data, response.data)

    @mock.patch(
        "user.authentication.JWTCustomAuthentication.authenticate",
        mock_authenticate_credentials_success(),
    )
    def test_search_post_all_success(self):
        response = self.client.get(f'{self.url}?q=')

        post_serializer = ListPostSerializer([self.post[0], self.post2[0]], many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post_serializer.data, response.data)

    def test_search_post_missing_auth(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
