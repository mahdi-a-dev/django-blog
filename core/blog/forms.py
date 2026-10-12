from django import forms
from .models import Post


class PostCreationForm(forms.ModelForm):
    """
    Represent a Post form for create and update.
    """
    class Meta:
        model = Post
        fields = ("title", "content", "image", "status", "category", "published_date")
