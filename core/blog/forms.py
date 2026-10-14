from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Represent a Post form for create and update.
    """
    class Meta:
        model = Post
        fields = ("title", "content", "image", "category")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)