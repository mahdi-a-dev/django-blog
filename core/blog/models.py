from django.db import models


class Post(models.Model):
    """
    This is a class to define post for blog app 
    """
    
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    status = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()
    
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ["-created_date"]
    

class Category(models.Model):
    """
    This is a class to define category of post for blog app 
    """
    name = models.CharField(max_length=250)
    
    
    def __str__(self):
        return self.name
