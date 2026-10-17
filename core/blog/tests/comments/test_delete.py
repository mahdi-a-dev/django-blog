from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post, Category, Comment
from django.urls import reverse

user = get_user_model()

class DeleteCommentTests(TestCase):
    """
    Test DeleteComment to only authenticated users can delete their comments
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
        
        cls.comment = Comment.objects.create(
            post=cls.post,
            profile=cls.profile,
            content="comment content"
        )
        
    def test_anonymous_user_redirect_to_login(self):
        """
        Test anonymous user connot delete comment and redirect to login
        """
        response = self.client.post(
            reverse(
                "blog:delete-comment",
                kwargs={"post_id": self.post.pk, "pk": self.comment.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(profile=self.profile).exists())
        
    def test_non_staff_user_can_delete_their_own_comments(self):
        """
        Test non staff user can delete their own comments
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse(
                "blog:delete-comment",
                kwargs={"post_id": self.post.pk, "pk": self.comment.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(profile=self.profile).exists())
        
    def test_non_staff_user_cannot_delete_other_users_comments(self):
        """
        Test non staff user cannot delete other users comments
        """
        regular_user = user.objects.create_user(
            email="other_regular@email.com",
            password="other_regular-password-123"
        )
                
        self.client.force_login(regular_user)
        
        response = self.client.post(
            reverse(
                "blog:delete-comment",
                kwargs={"post_id": self.post.pk, "pk": self.comment.pk}
            )
        )
        
        self.assertEqual(response.status_code, 404)