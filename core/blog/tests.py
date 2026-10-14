from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from accounts.models import Profile

user = get_user_model()

class PostModleTest(TestCase):
    
    def setUp(self):
        self.user = user.objects.create_user(
            email="test@email.com",
            password="test-password-123"
        )
        
        self.profile = self.user.profile
              
    def test_new_post_is_draft_by_default(self):
        post = Post.objects.create(
            author=self.profile,
            title = "Test post",
            content = "Test content"
        )
        
        self.assertFalse(post.status)
    
    def test_published_date_is_none_by_default(self):
        post = Post.objects.create(
            author=self.profile,
            title="Test post",
            content="Test content"
        )
        
        self.assertIsNone(post.published_date)
    
    def test_post_uses_default_image(self):
        post = Post.objects.create(
            author=self.profile,
            title="Test post",
            content="Test content"
        )
        
        self.assertEqual(post.image.name, "post_images/post_default_image.png")
