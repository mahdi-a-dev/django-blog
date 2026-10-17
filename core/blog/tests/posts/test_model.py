from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post

user = get_user_model()

class PostModleTest(TestCase):
    """
    Test post model
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = user.objects.create_user(
            email="test@email.com",
            password="test-password-123"
        )
        
        cls.profile = cls.user.profile

        cls.post = Post.objects.create(
            author=cls.profile,
            title = "Test post",
            content = "Test content"
        )
    
    def test_post_object_is_created_successfully(self):
        Post.objects.create(
            author=self.profile,
            title="New post",
            content="Post content"
        )
        
        self.assertTrue(Post.objects.filter(title="New post").exists())
        
              
    def test_new_post_is_unpublished_by_default(self):
        self.assertFalse(self.post.status)
    
    def test_published_date_is_none_by_default(self):
        self.assertIsNone(self.post.published_date)
