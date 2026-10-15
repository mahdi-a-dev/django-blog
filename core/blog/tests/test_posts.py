from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Post
from django.urls import reverse

user = get_user_model()

class PostListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = user.objects.create_user(
            email="test@email.com",
            password="test-password-123"
        )
        
        cls.profile = cls.user.profile
        
        for i in range(12):
            Post.objects.create(
                author=cls.profile,
                title=f"post {i}",
                content=f"content {i}",
                status=True
            )
        
    def test_only_published_posts_are_displayed(self):
        published_post = Post.objects.create(
            author=self.profile,
            title="Published post",
            content="Published post content",
            status=True
        )
        
        unpublished_post = Post.objects.create(
            author=self.profile,
            title="Unpublished post",
            content="Unpublished post content",
        )
        
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, published_post.title, msg_prefix="post list contains published posts")
        self.assertNotContains(response, unpublished_post.title, msg_prefix="post list not contains unpublished posts")
        
        
    def test_post_list_is_paginated(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(response.context["is_paginated"])
        
        
    def test_each_page_contains_ten_posts(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
        page_obj = response.context["page_obj"]
        
        self.assertEqual(len(page_obj.object_list), 10)


class PostDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = user.objects.create_user(
            email="test@email.com",
            password="test-password-123"
        )
        
        cls.profile = cls.user.profile
        
        cls.unpublished_post = Post.objects.create(
            author=cls.profile,
            title="Unpublished post",
            content="Unpublished content"
        )
        
        cls.published_post = Post.objects.create(
            author=cls.profile,
            title="Published post",
            content="Published content",
            status=True
        )
        
    def test_published_post_returnes_200(self):      
        response = self.client.get(
            reverse(
                "blog:post-detail", kwargs={"pk": self.published_post.pk}
                )
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_unpublished_post_returnes_404(self):      
        response = self.client.get(
            reverse(
                "blog:post-detail", kwargs={"pk": self.unpublished_post.pk}
                )
        )
    
        self.assertEqual(response.status_code, 404)
        
        