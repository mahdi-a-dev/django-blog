from django import forms
from .models import Post, Comment


class PostCreationForm(forms.ModelForm):
    """
    Represent a Post form for create and update.
    """
    class Meta:
        model = Post
        fields = ("title", "content", "image", "status", "category", "published_date")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)