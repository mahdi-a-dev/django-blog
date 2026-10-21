from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from blog.models import Post
from django.contrib.auth import get_user_model

user = get_user_model()

class PostDetailAPITests(APITestCase):
    """
    Test for post-detail api-view only staff user allowed to GET, PUT, DELETE method
    """
    
    def setUp(self):
        
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
        self.url = reverse("api:api-post-detail", kwargs={"pk": self.published_post.pk})
        
    def test_anonymous_user_cannot_access_post_details(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_non_staff_user_cannot_access_posts_details(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_staff_user_can_access_post_details(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn("published post", response.data["title"])
        
    def test_staff_user_can_update_posts(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.put(
            self.url,
            data={
                "author": self.profile.pk,
                "title": "new post",
                "content": "new content",
                "status": True
            },
            format="json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Post.objects.filter(title="new post").exists())
        
    def test_staff_user_can_delete_posts(self):
        self.client.force_authenticate(user=self.staff_user)

        response = self.client.delete(
            self.url,
            data={
                "id": self.published_post.pk
            },
            format="json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(author=self.profile).exists())
