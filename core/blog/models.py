from django.db import models
from accounts.models import User

class Post(models.Model):
    """
    This is a class to define post for blog app 
    """
    
    image = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()
    

class Category(models.Model):
    """
    This is a class to define category of post for blog app 
    """
    name = models.CharField(max_length=250)
    
    
    def __str__(self):
        return self.name
