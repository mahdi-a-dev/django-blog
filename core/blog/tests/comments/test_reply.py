from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post, Category, Comment
from django.urls import reverse

user = get_user_model()

class ReplyCommentTests(TestCase):
    """
    Test ReplyComment to only authenticated users can reply comments
    """
    @classmethod
    def setUpTestData(cls):
        # regular user
        cls.regular_user = user.objects.create_user(
            email="regular@email.com",
            password="regular-password-123"
        )
        
        cls.profile = cls.regular_user.profile
        
        cls.category = Category.objects.create(
            name="Test category",
            slug="Test category"
        )
        
        cls.post = Post.objects.create(
            author=cls.profile,
            title="published post",
            content="published post content",
            status=True
        )
        
        cls.parent_comment = Comment.objects.create(
            post=cls.post,
            profile=cls.profile,
            content="parent"
        )
        
    def setUp(self):
        # valid comment data for add comment
        self.comment_data = {
                "content": "Good post"
            }
        
    def test_anonymous_user_redirect_to_login(self):
        """
        Test anonymous user connot reply comment and redirect to login
        """
        response = self.client.post(
            reverse(
                "blog:reply-comment",
                kwargs={"post_id": self.post.pk, "pk": self.parent_comment.pk}
            ),
            data=self.comment_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(profile=self.profile, parent__isnull=False).exists())
        
    def test_non_staff_user_can_reply_comments(self):
        """
        Test non staff user can reply comment
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse(
                "blog:reply-comment",
                kwargs={"post_id": self.post.pk, "pk": self.parent_comment.pk}
            ),
            data=self.comment_data
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(profile=self.profile, parent__isnull=False).exists())