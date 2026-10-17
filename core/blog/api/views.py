from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from ..models import Post


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def post_list(request):
    # Show posts if method is GET
    if request.method == "GET":
        posts = get_list_or_404(Post, status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    # Save the giving post and show
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Show post if method is GET
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    # Update the giving post and show
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    # Delete giving post
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail": "item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
