from django.db import models
from django.urls import reverse


class Post(models.Model):
    """
    This is a class to define post for blog app 
    """
    
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to="post_images", null=True, blank=True)
    status = models.BooleanField(default=False)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, related_name="posts")

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    published_date = models.DateTimeField(null=True, blank=True)
    
    
    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.id})
    
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ["-created_date"]
    

class Category(models.Model):
    """
    This is a class to define category of post for blog app 
    """
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    
    
    def __str__(self):
        return self.name


class CommentManager(models.Manager):
    def parents(self):
        return self.filter(parent__isnull=True)
    
    
class Comment(models.Model):
    """
    This is a class to define comment of post for blog app 
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1000)
    
    # post replies
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    objects = CommentManager()

    
    def __str__(self):
        return f'Comment by {self.profile.user.email} on "{self.post.title}"'
    
    
    class Meta:
        ordering = ["-created_date"]
