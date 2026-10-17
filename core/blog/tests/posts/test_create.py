from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post, Category
from django.urls import reverse

user = get_user_model()

class PostCreateTests(TestCase):
    """
    Test PostCreate view for only staff users can create posts
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
        
        cls.category = Category.objects.create(
            name="Test category",
            slug="Test category"
        )
        
        
    def setUp(self):
        # valid post data for create post
        self.valid_post_data = {
                "title": "Django Testing",
                "content": "Learning Django",
                "category": self.category.pk
            }
        
    def test_anonymous_user_get_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with GET method
        """
        response = self.client.get(
            reverse("blog:post-create")
        )
        
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.post(
            reverse("blog:post-create"),
            data=self.valid_post_data
        )
        
        self.assertEqual(response.status_code, 302)
    
    def test_non_staff_user_cannot_access_create_post(self):
        """
        Test non staff user cannot access to postcreate with GET method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse("blog:post-create")
        )
        
        self.assertEqual(response.status_code, 403)

    def test_non_staff_user_cannot_create_post(self):
        """
        Test non staff user cannot access to postcreate with POST method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse("blog:post-create"),
            data=self.valid_post_data
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_can_access_create_post(self):
        """
        Test staff user can access to postcreate with GET method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse("blog:post-create")
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_staff_user_can_create_post(self):
        """
        Test staff user can access to postcreate with POST method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.post(
            reverse("blog:post-create"),
            data=self.valid_post_data
        )
                
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Post.objects.filter(title="Django Testing").exists()
        )
        
        
    def test_page_title_is_in_context(self):
        """
        Test page title (Create Post) is in postcreate context
        """
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse("blog:post-create")
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "title",
            response.context
        )
