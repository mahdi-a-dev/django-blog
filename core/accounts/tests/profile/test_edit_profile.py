from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from blog.models import Post
from ...models import Profile

user = get_user_model()

class EditProfileTests(TestCase):
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
                
        self.valid_profile_data = {
            "first_name": "my first name",
            "last_name": "my last name",
            "description": "my description"
        }
        
    def test_anonymous_user_get_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with GET method
        """
        response = self.client.get(
            reverse("accounts:edit-profile")
        )
        
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.get(
            reverse("accounts:edit-profile"),
            data=self.valid_profile_data
        )
        
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_can_access_edit_profile(self):
        """
        Test non staff user can access to edit profile
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse("accounts:edit-profile")
        )
        self.assertEqual(response.status_code, 200)
    
    def test_non_staff_user_can_edit_profile(self):
        """
        Test non staff user can edit profile
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse("accounts:edit-profile"),
            data=self.valid_profile_data
        )
        profile = Profile.objects.get(user=self.regular_user)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(profile.first_name, self.valid_profile_data["first_name"])
         
    def test_staff_user_can_access_edit_profile(self):
        """
        Test staff user can access to edit profile
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse("accounts:edit-profile")
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_staff_user_can_edit_profile(self):
        """
        Test staff user can edit profile
        """
        self.client.force_login(self.staff_user)
        
        
        response = self.client.post(
            reverse("accounts:edit-profile"),
            data=self.valid_profile_data
        )
        profile = Profile.objects.get(user=self.staff_user)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(profile.first_name, self.valid_profile_data["first_name"])
    
