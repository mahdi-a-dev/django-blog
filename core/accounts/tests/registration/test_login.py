from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ...forms import LoginForm

user = get_user_model()

class LoginTests(TestCase):
    """
    Test user login
    """
    def setUp(self):
        self.regular_user = user.objects.create_user(
            email="example@gmail.com",
            password="password-123"
        )
    
        self.assertTrue(user.objects.filter(email=self.regular_user.email).exists())

    def test_can_login(self):
        """
        test valid user logged in successfully.
        """ 
        response = self.client.post(
            reverse("accounts:login"),
            data={
                "username": "example@gmail.com",
                "password": "password-123"
            }
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get("_auth_user_id"))

    def test_login_data_is_valid(self):
        """
        Test login from is valid or invalid.
        """
        valid_form = LoginForm(data={
            "username": "example@gmail.com",
            "password": "password-123",
        })
        
        # invalid email
        invalid_email_form = LoginForm(data={
            "username": "invalidgmail.com",
            "password": "password-123",
        })
        
        # invalid password
        invalid_password_form = LoginForm(data={
            "username": "valid@gmail.com",
            "password": "password",
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
                "username": "myemail@gmail.com",
                "password": "password-123",
            }
        )
        
        # user with the same email
        form = LoginForm(data={
            "email": "myemail@gmail.com",
            "password": "password-123",
        })
        
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)