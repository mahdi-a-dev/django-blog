from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Post

user = get_user_model()

class ProfileTests(TestCase):
    """
    Test ProfileView, only authenticated user can access
    """
    def setUp(self):
        self.regular_user = user.objects.create_user(
            email="regular@gmail.com",
            password="password-123"
        )
        
        self.staff_user = user.objects.create_user(
            email="staff@gmail.com",
            password="password-123",
            is_staff=True
        )
        
        self.staff_profile = self.staff_user.profile
        
        self.staff_post = Post.objects.create(
            author=self.staff_profile,
            title="profile test post",
            content="profile test content"
        )
        
        
    def test_anonymous_user_redirect_to_login(self):
        """
        Test anonymous user get redirect to login
        """
        response = self.client.get(
            reverse("accounts:profile")
        )
        
        self.assertEqual(response.status_code, 302)

    
    def test_non_staff_user_cannot_access_staff_users_posts(self):
        """
        Test non staff user cannot access to staff users posts
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse("accounts:profile")
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("my_posts", response.context)
         
    def test_staff_user_can_access_their_posts(self):
        """
        Test staff user can access to their posts
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse("accounts:profile")
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.staff_post, response.context["my_posts"])

        
    def test_staff_user_cannot_access_another_staff_user_posts(self):
        """
        Test staff user cannot access to another staff user posts
        """
        staff_user = user.objects.create(
            email="anotherstaff@gmail.com",
            password="password-123",
            is_staff=True
        )
        self.client.force_login(staff_user)
        
        response = self.client.get(
            reverse("accounts:profile")
        )
        
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.staff_post, response.context["my_posts"])
    
    def test_superuser_can_accress_all_posts(self):
        """
        Test superuser canaccess to all posts
        """
        superuser = user.objects.create_superuser(
            email="superuser@gmail.com",
            password="password-123",
        )
        
        self.client.force_login(superuser)
        
        response = self.client.get(
            reverse("accounts:profile")
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.staff_post, response.context["my_posts"])