from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Post, Category
from django.urls import reverse
from ..forms import PostForm, CommentForm


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
        
    def test_each_page_contains_ten_posts(self):
        """
        Test postlist view is paginate by 10 post
        """
        response = self.client.get(
            reverse("blog:post-list")
        )
        self.assertEqual(response.status_code, 200)
        
        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj.object_list), 10)
    
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
        

class PostDetailTests(TestCase):
    """
    Test PostDetail view for display published post
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
        
        # published post with status == True
        cls.unpublished_post = Post.objects.create(
            author=cls.profile,
            title="Unpublished post",
            content="Unpublished content"
        )
        
        # unpublished post with status == False by default
        cls.published_post = Post.objects.create(
            author=cls.profile,
            title="Published post",
            content="Published content",
            status=True
        )
        
    def test_published_post_returnes_200(self):
        """
        Test postdetail only shows published posts and returns 200 status code
        """
        response = self.client.get(
            reverse(
                "blog:post-detail", kwargs={"pk": self.published_post.pk}
                )
        )
        
        self.assertEqual(response.status_code, 200)
        
    def test_unpublished_post_returnes_404(self):
        """
        Test postdetail does not show unpublished posts and returns 404 status code
        """
        response = self.client.get(
            reverse(
                "blog:post-detail", kwargs={"pk": self.unpublished_post.pk}
                )
        )
    
        self.assertEqual(response.status_code, 404)
        
    def test_comment_form_is_in_published_post_context(self):
        """
        Test postdetail only shows comment_form to authenticated users and returns 200 status code
        """
        response = self.client.get(
            reverse(
                "blog:post-detail", kwargs={"pk": self.published_post.pk}
                )
        )       
        
        self.assertEqual(response.status_code, 200)
        
        self.assertIn("comment_form", response.context)
        self.assertIsInstance(response.context["comment_form"], CommentForm)

    def test_comment_form_not_in_unpublished_post_context(self):
        """
        Test postdetail does not show comment_form to anonymous users and returns 404 status code
        """
        response = self.client.get(
            reverse(
                "blog:post-detail", kwargs={"pk": self.unpublished_post.pk}
                )
        )       
        
        self.assertEqual(response.status_code, 404)
        
        self.assertNotIn("comment_form", response.context)


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
        

class DeletePostTests(TestCase):
    """
    Test DeletePost view for only superusers can delete posts
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
        cls.staff_user_profile = cls.staff_user.profile
                
    def setUp(self):
        # staff user post
        self.post_created_by_staff = Post.objects.create(
            author=self.staff_user_profile,
            title="staff user post title",
            content="staff user post content"
        )
        
    def test_anonymous_user_get_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with GET method
        """
        response = self.client.get(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.post(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)
    
    def test_non_staff_user_cannot_access_delete_post(self):
        """
        Test non staff user cannot access to postdelete with GET method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.get(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 403)

    def test_non_staff_user_cannot_delete_post(self):
        """
        Test non staff user cannot access to postdelete with POST method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
                )
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_cannot_access_delete_post(self):
        """
        Test staff user cannot access to postdelete with GET method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.get(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_cannot_delete_post(self):
        """
        Test staff user cannot access to postdelete with POST method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.post(
            reverse(
                "blog:post-delete",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
                
        self.assertEqual(response.status_code, 403)
    
    def test_superusers_can_access_delete_post(self):
        """
        Test superusers can access to postdelete with GET method
        """
        self.client.force_login(self.super_user)
        
        response = self.client.get(
            reverse(
            "blog:post-delete",
            kwargs={"pk": self.post_created_by_staff.pk}),
        )
                
        self.assertEqual(response.status_code, 200)

    def test_supserusers_can_delete_post(self):
        """
        Test superusers can access to postdelete with POST method
        """
        
        self.client.force_login(self.super_user)
        
        response = self.client.post(
            reverse(
            "blog:post-delete",
            kwargs={"pk": self.post_created_by_staff.pk}),
        )
                
        self.assertEqual(response.status_code, 302)


class ChangeStatusPostTests(TestCase):
    """
    Test ChangeStatusPost view for only superusers can change status of posts
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
        cls.staff_user_profile = cls.staff_user.profile
                
    def setUp(self):
        # staff user post
        self.post_created_by_staff = Post.objects.create(
            author=self.staff_user_profile,
            title="staff user post title",
            content="staff user post content"
        )
        
    def test_anonymous_user_post_redirect_to_login(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
        
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_cannot_change_post_status(self):
        """
        Test non staff user cannot access to changestatuspost with POST method
        """
        self.client.force_login(self.regular_user)
        
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": self.post_created_by_staff.pk}
                )
        )
        
        self.assertEqual(response.status_code, 403)
        
    def test_staff_user_cannot_change_post_status(self):
        """
        Test staff user cannot access to changestatuspost with POST method
        """
        self.client.force_login(self.staff_user)
        
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": self.post_created_by_staff.pk}
            )
        )
                
        self.assertEqual(response.status_code, 403)

    def test_supserusers_can_change_post_status(self):
        """
        Test superusers can change post status with POST method
        """
        post = Post.objects.create(
            author=self.staff_user_profile,
            title="test",
            content="test",
            status=False
        )
        
        self.client.force_login(self.super_user)
        
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": post.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        
        # get post with True
        post = Post.objects.get(title="test", content="test")
        # check status == True and published date != None
        self.assertTrue(post.status == True)
        self.assertTrue(post.published_date != None)
        
        # send post request again to change status
        response = self.client.post(
            reverse(
                "blog:post-change-status",
                kwargs={"pk": post.pk}
            )
        )
        
        # get post with False
        post = Post.objects.get(title="test", content="test")
        # check status == False and published date == None
        self.assertTrue(post.status == False)
        self.assertTrue(post.published_date == None)
