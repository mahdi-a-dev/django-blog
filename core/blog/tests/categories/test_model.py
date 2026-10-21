from django.test import TestCase
from django.urls import reverse
from ...models import Category


class CategoyTest(TestCase):
    """
    Test category model
    """
    def setUp(self):
        self.category = Category.objects.create(
            name="Cinema",
            slug="Cinema"
        )
        
    def test_category_created_successfully(self):
        """
        Test category created succressfully.
        """
        self.assertTrue(Category.objects.filter(slug="Cinema").exists())

    def test_get_absolute_url(self):
        """
        Test get_absolute_url to be equal to post-detail url
        """
        self.assertEqual(
            self.category.get_absolute_url(),
            reverse("blog:category-posts", kwargs={"slug": self.category.slug})
        )
        