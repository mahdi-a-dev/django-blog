from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post
from django.urls import reverse

user = get_user_model()

class PostDetailTests(TestCase):
    """
    Test PostDetail view for display published post
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
        cls.profile = cls.staff_user.profile
        
        # published post with status == True
        cls.published_post = Post.objects.create(
            author=cls.profile,
            title="Published post",
            content="Published content",
            status=True
        )
        
        # unpublished post with status == False by default
        cls.unpublished_post = Post.objects.create(
            author=cls.profile,
            title="Unpublished post",
            content="Unpublished content"
        )
        
    def test_anonymous_user_can_access_published_posts(self):
        """
        Test anonymous user can access only published posts
        """
        response = self.client.get(
            reverse(
                "blog:post-detail",
                kwargs={"pk": self.published_post.pk}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_access_unpublished_posts(self):
        """
        Test anonymous user cannot access unpublished posts
        """
        response = self.client.get(
            reverse(
                "blog:post-detail",
                kwargs={"pk": self.unpublished_post.pk}
            )
        )
        self.assertEqual(response.status_code, 404)
    
    def test_non_staff_user_can_access_published_posts(self):
        """
        Test non staff user can access only published posts
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse(
                "blog:post-detail",
                kwargs={"pk": self.published_post.pk}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_non_staff_user_cannot_access_unpublished_post(self):
        """
        Test non staff user cannot access unpublished posts
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse(
                "blog:post-detail",
                kwargs={"pk": self.unpublished_post.pk}
                )
        )
        self.assertEqual(response.status_code, 404)
        
    def test_staff_user_can_access_published_posts(self):
        """
        Test staff user cannot access to published posts
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse(
                "blog:post-detail",
                kwargs={"pk": self.published_post.pk}
            )
        )
        
        self.assertEqual(response.status_code, 200)


    def test_staff_user_can_access_unpublished_posts_which_its_their_own(self):
        """
        Test staff user can access to unpublished posts which is their own
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse(
                "blog:post-detail",
                kwargs={"pk": self.unpublished_post.pk}
            )
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_staff_user_cannot_access_unpublished_posts_which_its_not_their_own(self):
        """
        Test staff user cannot access unpublished posts which its not their own
        """
        other_staff_user = user.objects.create_user(
            email="otherstaff@gmail.com",
            password="otherstaff@gmail.com",
            is_staff=True
        )
        
        profile = other_staff_user.profile
        
        unpublished_post = Post.objects.create(
            author=profile,
            title="unpublished",
            content="unpublished"
        )
        
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse(
                "blog:post-detail",
                kwargs={"pk": unpublished_post.pk}
            )
        )
                
        self.assertEqual(response.status_code, 404)
    
    def test_superusers_can_access_published_post(self):
        """
        Test superusers can access published posts
        """
        self.client.force_login(self.super_user)
        
        response = self.client.get(
            reverse(
            "blog:post-detail",
            kwargs={"pk": self.published_post.pk}),
        )
                
        self.assertEqual(response.status_code, 200)

    def test_supserusers_can_access_unpublished_posts(self):
        """
        Test superusers can access unpublished posts
        """
        
        self.client.force_login(self.super_user)
        
        response = self.client.get(
            reverse(
            "blog:post-detail",
            kwargs={"pk": self.unpublished_post.pk}),
        )
                
        self.assertEqual(response.status_code, 200)