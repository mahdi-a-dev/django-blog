from django.db import models
from django.urls import reverse


class Post(models.Model):
    """
    This is a class to define post for blog app 
    """
    
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images", default="static/asset/post_default_image.png")
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


class Comment(models.Model):
    """
    This is a class to define comment of post for blog app 
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'Comment by {self.profile.user.email} on "{self.post.title}"'
    
    
    class Meta:
        ordering = ["-created_date"]
