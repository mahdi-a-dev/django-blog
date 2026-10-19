from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ...forms import RegisterForm

user = get_user_model()

class RegisterTests(TestCase):
    """
    Test user registration
    """
    def test_can_registser(self):
        """
        test valid user save successfully.
        """
        self.client.post(
            reverse("accounts:register"),
            data={
                "email": "example@gmail.com",
                "password1": "password-123",
                "password2": "password-123"
            }
        )
        
        self.assertTrue(user.objects.filter(email="example@gmail.com").exists())
    
    def test_registeration_data_is_valid(self):
        """
        Test registration from is valid or invalid.
        """
        valid_form = RegisterForm(data={
            "email": "valid@gmail.com",
            "password1": "password-123",
            "password2": "password-123"    
        })
        
        # invalid email
        invalid_email_form = RegisterForm(data={
            "email": "invalidgmail.com",
            "password1": "password-123",
            "password2": "password-123"    
        })
        
        # invalid password
        invalid_password_form = RegisterForm(data={
            "email": "valid@gmail.com",
            "password1": "password",
            "password2": "password"    
        })
        
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_email_form.is_valid())
        self.assertFalse(invalid_password_form.is_valid())
        
    def test_duplicate_email_is_rejected(self):
        """
        Test duplicate email is rejected.
        """
        self.client.post(
            reverse("accounts:register"),
            data={
                "email": "example@gmail.com",
                "password1": "password-123",
                "password2": "password-123"
            }
        )
        
        # user with the same email
        form = RegisterForm(data={
            "email": "example@gmail.com",
            "password1": "password-123",
            "password2": "password-123"    
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)