from django.test import TestCase
from django.urls import reverse
from ...models import Post, Comment
from django.contrib.auth import get_user_model

user = get_user_model()


class CommentTest(TestCase):
    """
    Test Comment model
    """
    def setUp(self):
        self.user = user.objects.create_user(
            email="user@gmail.com",
            password="user-password-123"
        )
        
        self.profile = self.user.profile
        
        self.post = Post.objects.create(
            author=self.profile,
            title="post title",
            content="post content"
        )
        
        self.comment = Comment.objects.create(
            post=self.post,
            profile=self.profile,
            content="comment content"
        )
        
    def test_comment_created_successfully(self):
        """
        Test comment create successfully
        """
        self.assertTrue(Comment.objects.filter(
            profile=self.comment.profile,
            content=self.comment.content)
                        .exists()
        )
        
    def test_parent_is_null_by_default(self):
        """
        Test parent field is null by detault
        """
        self.assertIsNone(self.comment.parent)
        