from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post, Category
from django.urls import reverse

user = get_user_model()

class UpdatePostTests(TestCase):
    """
    Test PostUpdate view for only staff users can updata posts
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
        
        # user profile
        cls.staff_user_profile = cls.staff_user.profile
        
        cls.category = Category.objects.create(
            name="Test category",
            slug="Test category"
        )
             
    def setUp(self):
        # staff user post
        self.post_created_by_staff = Post.objects.create(
            author=self.staff_user_profile,
            title="staff user post title",
            content="staff user post content",
            status=True
        )
        
        # valid post data for update post
        self.valid_post_data = {
                "title": "Update Post Testing",
                "content": "Update Post Testing",
                "category": self.category.pk
            }
        
    def test_anonymous_user_get_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with GET method
        """
        response = self.client.get(
            reverse(
                "blog:post-edit",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.post(
            reverse("blog:post-edit", kwargs={"pk": self.post_created_by_staff.pk}),
            data=self.valid_post_data
        )
        
        self.assertEqual(response.status_code, 302)
    
    def test_non_staff_user_cannot_access_update_post(self):
        """
        Test non staff user cannot access to postupdate with GET method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse(
                "blog:post-edit",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 403)

    def test_non_staff_user_cannot_update_post(self):
        """
        Test non staff user cannot access to postupdate with POST method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse("blog:post-edit", kwargs={"pk": self.post_created_by_staff.pk}),
            data=self.valid_post_data
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_can_access_update_post(self):
        """
        Test staff user can access to postcreate with GET method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse(
                "blog:post-edit",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_staff_user_can_update_post(self):
        """
        Test staff user can access to postupdate with POST method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.post(
            reverse("blog:post-edit", kwargs={"pk": self.post_created_by_staff.pk}),
            data=self.valid_post_data
        )
                
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Post.objects.filter(title="Update Post Testing").exists()
        )
        
    def test_staff_user_cannot_update_another_staff_users_posts(self):
        """
        Test staff user cannot access to postupdate with POST method which post was created by another staff user
        """
        staff_user = user.objects.create_user(
            email="staff2@gmail.com",
            password="staff2@gmail.com",
            is_staff=True
        )
        profile = staff_user.profile
        
        post = Post.objects.create(
            author=profile,
            title="Another Staff User Post",
            content="Another Staff User Content"
        )
        
        self.client.force_login(self.staff_user)
        
        response = self.client.post(
            reverse("blog:post-edit", kwargs={"pk": post.pk}),
            data=self.valid_post_data
        )
                
        self.assertEqual(response.status_code, 404)
     
    def test_page_title_is_in_context(self):
        """
        Test page title (Update Post) is in postupdate context
        """
        self.client.force_login(self.staff_user)

        response = self.client.get(
            reverse(
                "blog:post-edit",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "title",
            response.context
        )