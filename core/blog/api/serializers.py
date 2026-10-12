from rest_framework import serializers
from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer Post model and show in Json format.
    """
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "status", "created_date", "published_date"]