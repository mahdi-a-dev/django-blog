from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from blog.models import Post
from django.contrib.auth import get_user_model

user = get_user_model()

class PostListAPITests(APITestCase):
    """
    Test for post-list api-view only staff user allowed to GET, POST method
    """
    
    def setUp(self):
        self.url = reverse("api:api-post-list")
        
        self.user = user.objects.create_user(
            email="author@gmail.com",
            password="test-password"
        )
        
        self.staff_user = user.objects.create_user(
            email="staff@gmail.com",
            password="test-password",
            is_staff=True
        )
        
        self.profile = self.user.profile
        
        self.published_post = Post.objects.create(
            author=self.profile,
            title="published post",
            content="published content",
            status=True
        )
    
    def test_anonymous_user_cannot_access_list_published_posts(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_non_staff_user_cannot_access_list_published_posts(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_user_can_access_list_published_posts(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [post["title"] for post in response.data]
        
        self.assertIn("published post", titles)

    def test_staff_user_can_create_posts(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.post(
            self.url,
            data={
                "author": self.profile.pk,
                "title": "new post",
                "content": "new content",
                "status": False
            },
            format="json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        