from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Represent a Post form for create and update.
    """    
    title = forms.CharField(
        max_length=250,
        widget=forms.TextInput,
        error_messages={
            "required": "Post title is required.",
            "max_length": "The title is too long."
        }
    )
    content = forms.CharField(
        max_length=30000,
        widget=forms.Textarea,
        error_messages={
            "required": "Post content is required."
        }
    )
    class Meta:
        model = Post
        fields = ("title", "content", "image", "category")


class CommentForm(forms.ModelForm):
    """
    Represent a Comment form for add and edit.
    """ 
    content = forms.CharField(
        max_length=1000, 
        widget=forms.Textarea,
        error_messages={
            "required": "Content is required."
        }
    )
    
    class Meta:
        model = Comment
        fields = ("content",)