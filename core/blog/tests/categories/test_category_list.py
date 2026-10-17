from django.test import TestCase
from django.contrib.auth import get_user_model
from ...models import Post, Category
from django.urls import reverse

user = get_user_model()

class CategoryPostListTests(TestCase):
    """
    Test CategoryPostList view for display posts form one category
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
                category=cls.category,
                status=True
            )
            
        # published post with status == True
        cls.published_post = Post.objects.create(
            author=cls.profile,
            title="published post",
            content="published post content",
            category=cls.category,
            status=True
        )
        
        # unpublished post with status == False by default
        cls.unpublished_post = Post.objects.create(
            author=cls.profile,
            title="unpublished post",
            content="unpublished post content",
            category=cls.category
        )
        
    def test_only_published_posts_are_displayed(self):
        """
        Test only published posts are in view
        """
        response = self.client.get(
            reverse(
                "blog:category-posts",
                kwargs={"slug": self.category.slug}
            )
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, self.published_post.title)
        self.assertNotContains(response, self.unpublished_post.title)
        
    def test_post_list_is_paginated(self):
        """
        Test categorypostlist view is paginated
        """
        response = self.client.get(
            reverse(                
                "blog:category-posts",
                kwargs={"slug": self.category.slug}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        
    def test_each_page_contains_nine_posts(self):
        """
        Test categorypostlist view is paginate by 9 post
        """
        response = self.client.get(
            reverse(
                "blog:category-posts",
                kwargs={"slug": self.category.slug}
            )
        )
        self.assertEqual(response.status_code, 200)
        
        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj.object_list), 9)
        
