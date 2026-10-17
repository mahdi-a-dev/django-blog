from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post
from django.urls import reverse

user = get_user_model()

class DeletePostTests(TestCase):
    """
    Test DeletePost view for only superusers can delete posts
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
        
    def test_anonymous_user_get_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with GET method
        """
        response = self.client.get(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.post(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)
    
    def test_non_staff_user_cannot_access_delete_post(self):
        """
        Test non staff user cannot access to postdelete with GET method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 403)

    def test_non_staff_user_cannot_delete_post(self):
        """
        Test non staff user cannot access to postdelete with POST method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
                )
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_cannot_access_delete_post(self):
        """
        Test staff user cannot access to postdelete with GET method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_cannot_delete_post(self):
        """
        Test staff user cannot access to postdelete with POST method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.post(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
                
        self.assertEqual(response.status_code, 403)
    
    def test_superusers_can_access_delete_post(self):
        """
        Test superusers can access to postdelete with GET method
        """
        self.client.force_login(self.super_user)
        
        response = self.client.get(
            reverse(
            "blog:post-delete",
            kwargs={"pk": self.post_created_by_staff.pk}),
        )
                
        self.assertEqual(response.status_code, 200)

    def test_supserusers_can_delete_post(self):
        """
        Test superusers can access to postdelete with POST method
        """
        
        self.client.force_login(self.super_user)
        
        response = self.client.post(
            reverse(
            "blog:post-delete",
            kwargs={"pk": self.post_created_by_staff.pk}),
        )
                
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(author=self.staff_user_profile).exists())