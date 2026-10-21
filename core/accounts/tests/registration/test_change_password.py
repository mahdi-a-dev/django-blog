from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Post
from ...models import Profile

user = get_user_model()

class PasswordChangeTests(TestCase):
    """
    Test ChangePassword, only authenticated user can access
    """
    @classmethod
    def setUpTestData(self):
        self.regular_user = user.objects.create_user(
            email="regular@gmail.com",
            password="password-123"
        )
        
        self.staff_user = user.objects.create_user(
            email="staff@gmail.com",
            password="password-123",
            is_staff=True
        )
                
        self.valid_change_password_data = {
            "old_password": "password-123",
            "new_password1": "my_new_password-1",
            "new_password2": "my_new_password-1"
        }
        
    def test_anonymous_user_get_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with GET method
        """
        response = self.client.get(
            reverse("accounts:password-change")
        )
        
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.post(
            reverse("accounts:password-change"),
            data=self.valid_change_password_data
        )
        
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_can_access_password_change(self):
        """
        Test non staff user can access to passwordchange
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse("accounts:password-change")
        )
        self.assertEqual(response.status_code, 200)
    
    def test_non_staff_user_can_change_password(self):
        """
        Test non staff user can change password
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse("accounts:password-change"),
            data=self.valid_change_password_data
        )
        regular_user = user.objects.get(email=self.regular_user.email)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(regular_user.check_password(self.valid_change_password_data["new_password1"]))
         
    def test_staff_user_can_access_password_change(self):
        """
        Test staff user can access to passwordchange
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse("accounts:password-change")
        )
        self.assertEqual(response.status_code, 200)
        
    def test_staff_user_can_change_password(self):
        """
        Test staff user can change password
        """
        self.client.force_login(self.staff_user)
        
        
        response = self.client.post(
            reverse("accounts:password-change"),
            data=self.valid_change_password_data
        )
        staff_user = user.objects.get(email=self.staff_user.email)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(staff_user.check_password(self.valid_change_password_data["new_password1"]))
    