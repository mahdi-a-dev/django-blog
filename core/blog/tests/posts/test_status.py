from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post
from django.urls import reverse

user = get_user_model()

class ChangeStatusPostTests(TestCase):
    """
    Test ChangeStatusPost view for only superusers can change status of posts
    """
    @classmethod
    def setUpTestData(cls):
        # regular user
        cls.regular_user = user.objects.create_user(
            email="regular@email.com",
            password="regular-password-123"
        )
        
        # staff user
        cls.staff_user = user.objects.create_user(
            email="staff@gmail.com",
            password="staff@gmail.com",
            is_staff=True
        )
        
        # superuser
        cls.super_user = user.objects.create_user(
            email="superuser@gmail.com",
            password="supseruser@gmail.com",
            is_staff=True,
            is_superuser=True
        )
        
        # user profile
        cls.staff_user_profile = cls.staff_user.profile
                
    def setUp(self):
        # staff user post
        self.post_created_by_staff = Post.objects.create(
            author=self.staff_user_profile,
            title="staff user post title",
            content="staff user post content"
        )
        
    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_cannot_change_post_status(self):
        """
        Test non staff user cannot access to changestatuspost with POST method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": self.post_created_by_staff.pk}
                )
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_cannot_change_post_status(self):
        """
        Test staff user cannot access to changestatuspost with POST method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
                
        self.assertEqual(response.status_code, 403)

    def test_supserusers_can_change_post_status(self):
        """
        Test superusers can change post status with POST method
        """
        post = Post.objects.create(
            author=self.staff_user_profile,
            title="test",
            content="test",
            status=False
        )
        
        self.client.force_login(self.super_user)
        
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": post.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        
        # get post with True
        post = Post.objects.get(title="test", content="test")
        # check status == True and published date != None
        self.assertTrue(post.status == True)
        self.assertTrue(post.published_date != None)
        
        # send post request again to change status
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": post.pk}
            )
        )
        
        # get post with False
        post = Post.objects.get(title="test", content="test")
        # check status == False and published date == None
        self.assertTrue(post.status == False)
        self.assertTrue(post.published_date == None)
