from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post, Category
from django.urls import reverse

user = get_user_model()

class PostListTests(TestCase):
    """
    Test PostList view for display published posts
    """
    @classmethod
    def setUpTestData(cls):
        # regular user
        cls.user = user.objects.create_user(
            email="test@email.com",
            password="test-password-123"
        )
        
        # user profile
        cls.profile = cls.user.profile

        cls.category = Category.objects.create(
            name="cinema",
            slug="cinema"
        )
        
        
        # create 12 posts for testing pagination
        for i in range(12):
            Post.objects.create(
                author=cls.profile,
                title=f"post {i}",
                content=f"content {i}",
                status=True
            )
            
        # published post with status == True
        cls.published_post = Post.objects.create(
            author=cls.profile,
            title="published post",
            content="published post content",
            status=True
        )
        
        # unpublished post with status == False by default
        cls.unpublished_post = Post.objects.create(
            author=cls.profile,
            title="unpublished post",
            content="unpublished post content",
        )
        
    def test_only_published_posts_are_displayed(self):
        """
        Test only published posts are in post-list view
        """
        response = self.client.get(
            reverse("blog:post-list")
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, self.published_post.title)
        self.assertNotContains(response, self.unpublished_post.title)
        
    def test_post_list_is_paginated(self):
        """
        Test postlist view is paginated
        """
        response = self.client.get(
            reverse("blog:post-list")
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        
    def test_each_page_contains_nine_posts(self):
        """
        Test postlist view is paginate by 10 post
        """
        response = self.client.get(
            reverse("blog:post-list")
        )
        self.assertEqual(response.status_code, 200)
        
        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj.object_list), 9)
    
    def test_search_returns_matching_published_posts(self):
        """
        Test postlist search returns the match title
        """
        response = self.client.get(
            reverse("blog:post-list") + "?s=published"
        )
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.published_post.title)
        self.assertNotContains(response, self.unpublished_post.title)
            
    def test_categories_are_in_context(self):
        """
        Test categories are in post-list view context
        """
        response = self.client.get(
            reverse("blog:post-list")
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            self.category,
            response.context["categories"]
        )
        