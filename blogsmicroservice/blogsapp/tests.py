from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from blogsmicroservice.blogsapp.models import BlogPost
from rest_framework.authtoken.models import Token

class BlogsMicroserviceTests(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            body='This is a test blog post.',
            author=self.user
        )

    def test_signup(self):
        url = reverse('signup')
        data = {'username': 'another', 'password': 'pass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_signin(self):
        url = reverse('signin')
        data = {'username': 'testuser', 'password': 'pass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_list_blog_post(self):
        url = reverse('blogpost-list')
        self.client.credentials() #Do not require credentials
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_create_blog_post(self):
        url = reverse('blogpost-list')
        data = {'title': 'Blog Post Title', 'body': 'Content of the post.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Blog Post Title')
        self.assertEqual(response.data['author'], self.user.username)

    def test_get_blog_post(self):
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.pk})
        self.client.credentials() #Do not require credentials
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.blog_post.title)

    def test_update_blog_post(self):
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.pk})
        data = {'title': 'Updating title', 'body': 'Updating body'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updating title')

    def test_partial_update_blog_post(self):
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.pk})
        data = {'title': 'Updating only title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updating only title')

    def test_delete_blog_post(self):
        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.blog_post.refresh_from_db()
        self.assertIsNotNone(self.blog_post.deleted_at)

    def test_create_blog_post_unauthenticated(self):
        url = reverse('blogpost-list')
        self.client.credentials()
        data = {'title': 'Blog Post Title', 'content': 'Content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_blog_post_not_author(self):
        new_user = User.objects.create_user(username='newuser', password='pass')
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.pk})
        data = {'title': 'Updating Blog Post', 'body': 'Updating body'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_blog_post_not_author(self):
        new_user = User.objects.create_user(username='newuser', password='pass')
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.pk})
        data = {'title': 'Updating only Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_blog_post_not_author(self):
        new_user = User.objects.create_user(username='newuser', password='pass')
        new_token = Token.objects.create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token.key)

        url = reverse('blogpost-detail', kwargs={'pk': self.blog_post.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
